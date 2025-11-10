import customtkinter as ctk
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import datetime

CATEGORY_ICONS = {
    "General": "⚙️",
    "SERVIDORES": "💻",
    "ANTENAS": "📶",
    "SWITCHES": "🔄",
    "HOSTS-CRÍTICOS": "🖥️",
    "Default": "⚙️"
}

CATEGORY_COLORS = {
    "General": "#607D8B",
    "SERVIDORES": "#4CAF50",
    "ANTENAS": "#2196F3",
    "SWITCHES": "#FFC107",
    "HOSTS-CRÍTICOS": "#F44336",
    "Default": "#9E9E9E"
}

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, api_client, monitoring_service=None):
        super().__init__(parent, corner_radius=0)
        self.api_client = api_client
        self.monitoring_service = monitoring_service
        self.categories = []
        self.host_widgets = {}
        self.is_destroyed = False

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1) # Left host list
        self.grid_columnconfigure(1, weight=2) # Right content area
        self.grid_rowconfigure(2, weight=1) # Main content row

        # --- Title ---
        self.title_label = ctk.CTkLabel(self, text="Dashboard Principal", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        # --- Summary Frames ---
        self.summary_frame = ctk.CTkFrame(self)
        self.summary_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.summary_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) # 5 columns now

        self.hosts_frame = self.create_summary_frame(self.summary_frame, "Total de Hosts", "--")
        self.hosts_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.active_hosts_frame = self.create_summary_frame(self.summary_frame, "Hosts Activos", "--")
        self.active_hosts_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.inactive_hosts_frame = self.create_summary_frame(self.summary_frame, "Hosts Inactivos", "--")
        self.inactive_hosts_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # New Sede Summary Frame in the top row
        self.sede_summary_frame = ctk.CTkFrame(self.summary_frame)
        self.sede_summary_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.alerts_frame = self.create_summary_frame(self.summary_frame, "Alertas Activas", "--")
        self.alerts_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        # --- Left Panel: Host List ---
        self.host_scrollable_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Dispositivos Monitoreados",
            label_font=ctk.CTkFont(size=16, weight="bold")
        )
        self.host_scrollable_frame.grid(row=2, column=0, padx=(20, 5), pady=(0, 20), sticky="nsew")
        self.host_scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Right Panel: Content Area ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=1, padx=(5, 20), pady=(0, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1) # Chart frame will expand
        
        # --- Chart Frame ---
        self.chart_frame = ctk.CTkFrame(self.content_frame)
        self.chart_frame.grid(row=0, column=0, sticky="nsew") # Changed from row=1
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(1, weight=1)

        self.chart_title_label = ctk.CTkLabel(self.chart_frame, text="Distribución de Hosts por Estado", font=ctk.CTkFont(size=16, weight="bold"))
        self.chart_title_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.load_initial_data()

    def destroy(self):
        self.is_destroyed = True
        super().destroy()

    def create_summary_frame(self, parent, title, value):
        frame = ctk.CTkFrame(parent)
        frame.grid_columnconfigure(0, weight=1)
        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        title_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=36, weight="bold"))
        value_label.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="w")
        frame.value_label = value_label
        return frame

    def load_initial_data(self):
        self.display_loading_info()
        thread = threading.Thread(target=self.fetch_and_display_initial_data)
        thread.daemon = True
        thread.start()

    def fetch_and_display_initial_data(self):
        try:
            hosts = self.api_client.get_hosts()
            categorias = self.api_client.get_categorias()
            alerts = self.api_client.get_active_alerts()
            sedes = self.api_client.get_sedes()
            if not self.is_destroyed:
                self.after(0, self.setup_ui_with_data, hosts, categorias, alerts, sedes)
        except Exception as e:
            print(f"Failed to fetch initial data: {e}")
            if not self.is_destroyed:
                self.after(0, self.display_error_info)

    def setup_ui_with_data(self, hosts, categorias, alerts, sedes):
        self.categories = categorias if categorias is not None else []
        self.update_host_list(hosts, {}) 
        self.update_pie_chart(hosts)
        self.update_sede_summary(hosts, sedes)
        
        total_hosts = len(hosts) if hosts else 0
        active_hosts = len([h for h in hosts if h and h.get('estado', {}).get('NOM_ESTADO') == 'Activo']) if hosts else 0
        inactive_hosts = total_hosts - active_hosts
        active_alerts = len(alerts) if alerts else 0
        self.update_summary_values(total_hosts, active_hosts, inactive_hosts, active_alerts)

    def update_dashboard(self, realtime_ping_results):
        hosts = self.api_client.get_hosts()
        alerts = self.api_client.get_active_alerts()
        sedes = self.api_client.get_sedes()
        if hosts:
            self.update_host_list(hosts, realtime_ping_results)
            self.update_sede_summary(hosts, sedes)
            
            total_hosts = len(hosts)
            active_hosts_count = sum(1 for host in hosts if realtime_ping_results.get(host.get("ID_HOST")) is not None)
            inactive_hosts_count = total_hosts - active_hosts_count
            alerts_count = len(alerts) if alerts else self.alerts_frame.value_label.cget("text")

            self.update_summary_values(total_hosts, active_hosts_count, inactive_hosts_count, alerts_count)

            if self.chart_title_label.cget("text") == "Distribución de Hosts por Estado":
                 self.update_pie_chart(hosts)

    def update_summary_values(self, total, active, inactive, alerts):
        self.hosts_frame.value_label.configure(text=str(total))
        self.active_hosts_frame.value_label.configure(text=str(active), text_color="#7CFC00")
        self.inactive_hosts_frame.value_label.configure(text=str(inactive), text_color="#EA4335")
        self.alerts_frame.value_label.configure(text=str(alerts))

    def update_sede_summary(self, hosts, sedes):
        print(f"DEBUG: update_sede_summary called with hosts: {hosts}")
        print(f"DEBUG: update_sede_summary called with sedes: {sedes}")

        for widget in self.sede_summary_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.sede_summary_frame, text="Hosts por Sede", font=ctk.CTkFont(size=14))
        title_label.pack(anchor="w", padx=20, pady=(10, 5))

        if not hosts or not sedes:
            ctk.CTkLabel(self.sede_summary_frame, text="No hay datos.").pack(anchor="w", padx=20, pady=5)
            return

        sede_id_to_name = {s["ID_SEDE"]: s["NOM_SEDE"] for s in sedes}
        print(f"DEBUG: sede_id_to_name: {sede_id_to_name}")
        host_counts = defaultdict(int)
        for host in hosts:
            if host and host.get("ID_SEDE") in sede_id_to_name:
                host_counts[host["ID_SEDE"]] += 1
        print(f"DEBUG: host_counts: {host_counts}")

        if not host_counts:
            ctk.CTkLabel(self.sede_summary_frame, text="No hay hosts asignados.").pack(anchor="w", padx=20, pady=5)
            return

        # Use a scrollable frame inside if the list can be long
        content_frame = ctk.CTkFrame(self.sede_summary_frame, fg_color="transparent")
        content_frame.pack(fill="x", expand=True, padx=20, pady=5)

        row = 0
        for sede_id, count in sorted(host_counts.items()):
            sede_name = sede_id_to_name.get(sede_id, "Desconocida")
            label = ctk.CTkLabel(content_frame, text=f"{sede_name}: {count}", font=ctk.CTkFont(size=12))
            label.grid(row=row, column=0, sticky="w")
            row += 1

    def update_host_list(self, hosts, realtime_ping_results):
        for widget in self.host_scrollable_frame.winfo_children():
            widget.destroy()
        self.host_widgets.clear()

        if not hosts:
            ctk.CTkLabel(self.host_scrollable_frame, text="No se encontraron hosts.").pack(pady=10)
            return

        hosts_by_category = defaultdict(list)
        for host in hosts:
            if host:
                hosts_by_category[host.get("ID_CATEGORIA")].append(host)

        category_names = {cat.get("ID_CATEGORIA"): cat.get("NOM_CATEGORIA", "Sin Categoría") for cat in self.categories}
        
        for cat_id, cat_name in sorted(category_names.items(), key=lambda item: item[1]):
            if cat_id in hosts_by_category:
                icon = CATEGORY_ICONS.get(cat_name, CATEGORY_ICONS["Default"])
                color = CATEGORY_COLORS.get(cat_name, CATEGORY_COLORS["Default"])
                cat_label = ctk.CTkLabel(self.host_scrollable_frame, text=f"{icon} {cat_name}", font=ctk.CTkFont(size=14, weight="bold"), text_color=color)
                cat_label.pack(fill="x", padx=10, pady=(10, 5), anchor="w")

                for host in sorted(hosts_by_category[cat_id], key=lambda h: h.get('NOM_HOST', '')):
                    host_id = host.get("ID_HOST")
                    host_name = host.get('NOM_HOST', 'N/A')
                    
                    ping_result = realtime_ping_results.get(host_id)
                    status_text, status_color = self._get_realtime_status_info(ping_result)

                    host_button = ctk.CTkButton(
                        self.host_scrollable_frame,
                        text=f"{host_name} - {status_text}",
                        text_color=status_color,
                        fg_color="transparent",
                        hover_color=("gray85", "gray15"),
                        anchor="w",
                        command=lambda h=host: self.show_host_ping_chart(h)
                    )
                    host_button.pack(fill="x", padx=20, pady=0, ipady=0)
                    self.host_widgets[host_id] = host_button

    def show_host_ping_chart(self, host):
        self.chart_title_label.configure(text=f"Ping Diario: {host.get('NOM_HOST')}")
        self.ax.clear()
        self.ax.set_facecolor('#2B2B2B')
        self.fig.patch.set_facecolor('#2B2B2B')
        self.ax.text(0.5, 0.5, "Cargando datos de ping...", color="white", ha="center", va="center")
        self.canvas.draw()

        thread = threading.Thread(target=self._fetch_and_draw_ping_chart, args=(host,))
        thread.daemon = True
        thread.start()

    def _fetch_and_draw_ping_chart(self, host):
        try:
            host_id = host.get("ID_HOST")
            today = datetime.date.today()
            start_date = today.strftime("%Y-%m-%d")
            
            ping_data = self.api_client.get_monitoreo_by_host(host_id, start_date=start_date)
            
            if not self.is_destroyed:
                self.after(0, self._draw_ping_chart, ping_data, host)
        except Exception as e:
            print(f"Error fetching ping data for host {host.get('ID_HOST')}: {e}")
            if not self.is_destroyed:
                self.after(0, self.display_chart_error, "Error al cargar datos de ping.")

    def _draw_ping_chart(self, ping_data, host):
        self.ax.clear()
        self.ax.set_facecolor('#2B2B2B')
        self.fig.patch.set_facecolor('#2B2B2B')

        if not ping_data:
            self.ax.text(0.5, 0.5, "No hay datos de ping para hoy.", color="white", ha="center", va="center")
        else:
            timestamps = [datetime.datetime.fromisoformat(p['TIMESTAMP']) for p in ping_data if p['PING_RESULT'] is not None]
            pings = [p['PING_RESULT'] for p in ping_data if p['PING_RESULT'] is not None]

            if not pings:
                 self.ax.text(0.5, 0.5, "No hay datos de ping para hoy.", color="white", ha="center", va="center")
            else:
                self.ax.plot(timestamps, pings, marker='o', linestyle='-', color='#1F6AA5')
                self.ax.set_title(f"Ping Diario: {host.get('NOM_HOST')}", color='white', fontsize=14, weight='bold')
                self.ax.set_ylabel("Ping (ms)", color='white')
                self.ax.tick_params(axis='x', colors='white', rotation=45)
                self.ax.tick_params(axis='y', colors='white')
                for spine in self.ax.spines.values():
                    spine.set_edgecolor('white')
                self.ax.set_facecolor('#242424')

        self.fig.tight_layout()
        self.canvas.draw()

    def update_pie_chart(self, hosts):
        self.chart_title_label.configure(text="Distribución de Hosts por Estado")
        self.ax.clear()
        self.ax.set_facecolor('#2B2B2B')
        self.fig.patch.set_facecolor('#2B2B2B')

        if not hosts:
            self.ax.text(0.5, 0.5, "Sin datos de hosts", ha="center", va="center", color="white")
            self.canvas.draw()
            return

        active_hosts = len([h for h in hosts if h and h.get('estado', {}).get('NOM_ESTADO') == 'Activo'])
        inactive_hosts = len(hosts) - active_hosts
        
        labels = ['Activos', 'Inactivos']
        sizes = [active_hosts, inactive_hosts]
        colors = ['#1F6AA5', '#FF4D4D']
        
        if sum(sizes) > 0:
            self.ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
                        textprops={'color': 'white', 'fontsize': 10, 'weight': 'bold'},
                        pctdistance=0.85, wedgeprops=dict(width=0.4, edgecolor='w'))
            self.ax.axis('equal')
        else:
            self.ax.text(0.5, 0.5, "Sin datos de hosts", ha="center", va="center", color="white")

        self.canvas.draw()

    def _get_realtime_status_info(self, ping_result):
        if ping_result is not None and ping_result >= 0:
            return f"Activo ({ping_result:.2f}ms)", "#7CFC00"
        return "Inactivo", "#EA4335"

    def display_loading_info(self):
        self.update_summary_values("...", "...", "...", "...")
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Cargando...", ha="center", va="center", color="white")
        self.canvas.draw()
        ctk.CTkLabel(self.host_scrollable_frame, text="Cargando hosts...").pack(pady=10)

    def display_error_info(self):
        self.update_summary_values("Error", "Error", "Error", "Error")
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Error al cargar datos", ha="center", va="center", color="red")
        self.canvas.draw()
        for widget in self.host_scrollable_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.host_scrollable_frame, text="Error al cargar hosts.").pack(pady=10)

    def display_chart_error(self, message):
        self.ax.clear()
        self.ax.text(0.5, 0.5, message, ha="center", va="center", color="red")
        self.canvas.draw()
