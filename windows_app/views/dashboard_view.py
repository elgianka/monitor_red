import customtkinter as ctk
import threading

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.api_client = api_client

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Dashboard Principal", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=30, pady=(30, 10), sticky="w")

        # Summary Frames
        self.summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.summary_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.summary_frame.grid_columnconfigure((0, 1), weight=1)

        self.hosts_frame = self.create_summary_frame(self.summary_frame, "Total de Hosts", "--")
        self.hosts_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.alerts_frame = self.create_summary_frame(self.summary_frame, "Alertas Activas", "--")
        self.alerts_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Content Frames (Alerts & Hosts)
        self.alerts_section_label = ctk.CTkLabel(self, text="Alertas Activas Recientes", font=ctk.CTkFont(size=16, weight="bold"))
        self.alerts_section_label.grid(row=2, column=0, padx=30, pady=(20, 5), sticky="w")
        
        self.alerts_scrollable_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.alerts_scrollable_frame.grid(row=3, column=0, padx=(30, 15), pady=10, sticky="nsew")

        self.hosts_section_label = ctk.CTkLabel(self, text="Todos los Hosts", font=ctk.CTkFont(size=16, weight="bold"))
        self.hosts_section_label.grid(row=2, column=1, padx=30, pady=(20, 5), sticky="w")

        self.hosts_scrollable_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.hosts_scrollable_frame.grid(row=3, column=1, padx=(15, 30), pady=10, sticky="nsew")

        # Load data and set up auto-refresh
        self.load_data_thread()
        self.after(300000, self.auto_refresh) # Auto-refresh every 5 minutes (300000 ms)

    def create_summary_frame(self, parent, title, value):
        frame = ctk.CTkFrame(parent)
        frame.grid_columnconfigure(0, weight=1)
        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        title_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=36, weight="bold"))
        value_label.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="w")
        frame.value_label = value_label
        return frame

    def load_data_thread(self, is_refresh=False):
        if not is_refresh:
            self.update_summary_values("Cargando...", "Cargando...")
            self.display_loading_in_alerts_frame()
            self.display_loading_in_hosts_frame()

        thread = threading.Thread(target=self.fetch_and_display_data)
        thread.daemon = True
        thread.start()

    def fetch_and_display_data(self):
        try:
            hosts = self.api_client.get_hosts()
            alerts = self.api_client.get_active_alerts()
            self.after(0, self.update_ui, hosts, alerts)
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            self.after(0, self.update_ui, None, None)

    def update_ui(self, hosts, alerts):
        total_hosts = len(hosts) if hosts is not None else "Error"
        active_alerts = len(alerts) if alerts is not None else "Error"
        self.update_summary_values(total_hosts, active_alerts)
        self.update_alerts_frame(alerts)
        self.update_hosts_frame(hosts)

    def update_summary_values(self, hosts_count, alerts_count):
        self.hosts_frame.value_label.configure(text=str(hosts_count))
        self.alerts_frame.value_label.configure(text=str(alerts_count))

    def display_loading_in_alerts_frame(self):
        self.clear_frame(self.alerts_scrollable_frame)
        ctk.CTkLabel(self.alerts_scrollable_frame, text="Cargando alertas...").pack(pady=10)

    def display_loading_in_hosts_frame(self):
        self.clear_frame(self.hosts_scrollable_frame)
        ctk.CTkLabel(self.hosts_scrollable_frame, text="Cargando hosts...").pack(pady=10)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def update_alerts_frame(self, alerts):
        self.clear_frame(self.alerts_scrollable_frame)
        if alerts:
            for alert in alerts:
                host_name = alert.get('host', {}).get('H_NOM', 'N/A')
                proceso = alert.get('proceso', {}).get('P_NOM', 'N/A')
                fecha = alert.get('AL_FECHA_REGISTRO', 'N/A')
                alert_entry = ctk.CTkFrame(self.alerts_scrollable_frame, border_width=1, border_color="#555555")
                alert_entry.pack(fill="x", expand=True, padx=10, pady=5)
                label = ctk.CTkLabel(alert_entry, text=f"🚨 Host: {host_name} | Proceso: {proceso}", anchor="w")
                label.pack(fill="x", padx=10, pady=10)
        elif alerts is not None:
            ctk.CTkLabel(self.alerts_scrollable_frame, text="No hay alertas activas.").pack(pady=10)
        else:
            ctk.CTkLabel(self.alerts_scrollable_frame, text="Error al cargar las alertas.").pack(pady=10)

    def update_hosts_frame(self, hosts):
        self.clear_frame(self.hosts_scrollable_frame)
        if hosts:
            for host in hosts:
                host_name = host.get('H_NOM', 'N/A')
                ip = host.get('H_IP', 'N/A')
                estado = host.get('estado', {}).get('E_NOM', 'N/A')
                host_entry = ctk.CTkFrame(self.hosts_scrollable_frame)
                host_entry.pack(fill="x", expand=True, padx=10, pady=5)
                label_text = f"💻 {host_name} ({ip}) - Estado: {estado}"
                label = ctk.CTkLabel(host_entry, text=label_text, anchor="w")
                label.pack(fill="x", padx=10, pady=10)
        elif hosts is not None:
            ctk.CTkLabel(self.hosts_scrollable_frame, text="No se encontraron hosts.").pack(pady=10)
        else:
            ctk.CTkLabel(self.hosts_scrollable_frame, text="Error al cargar los hosts.").pack(pady=10)

    def auto_refresh(self):
        print("Auto-refreshing dashboard data...")
        self.load_data_thread(is_refresh=True)
        self.after(300000, self.auto_refresh) # Reschedule after 5 minutes
