import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class HostDetailView(ctk.CTkFrame):
    def __init__(self, parent, api_client, host_id):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.api_client = api_client
        self.host_id = host_id

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.title_label = ctk.CTkLabel(self, text=f"Detalles del Host: {host_id}", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")

        # Frame for host details
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")

        # Date range selection
        date_range_frame = ctk.CTkFrame(self.details_frame)
        date_range_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(date_range_frame, text="Fecha Inicio:").pack(side="left", padx=(0, 5))
        self.start_date_entry = ctk.CTkEntry(date_range_frame, width=100)
        self.start_date_entry.pack(side="left", padx=(0, 10))
        self.start_date_entry.insert(0, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"))

        ctk.CTkLabel(date_range_frame, text="Fecha Fin:").pack(side="left", padx=(0, 5))
        self.end_date_entry = ctk.CTkEntry(date_range_frame, width=100)
        self.end_date_entry.pack(side="left", padx=(0, 10))
        self.end_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        filter_button = ctk.CTkButton(date_range_frame, text="Filtrar", command=self.load_monitoreo_data)
        filter_button.pack(side="left")

        # Frame for plot
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_frame.grid_rowconfigure(0, weight=1)


        self.load_host_details()
        self.load_monitoreo_data()

    def load_host_details(self):
        # Clear previous details
        for widget in self.details_frame.winfo_children():
            if not isinstance(widget, ctk.CTkFrame): # Don't destroy the date range frame
                widget.destroy()

        # Fetch host details from API
        host = self.api_client.get_host(self.host_id)
        if host:
            ctk.CTkLabel(self.details_frame, text=f"Nombre: {host.get('NOM_HOST', 'N/A')}").pack(anchor="w", padx=10, pady=5)
            ctk.CTkLabel(self.details_frame, text=f"IP: {host.get('IP_HOST', 'N/A')}").pack(anchor="w", padx=10, pady=5)
            estado = (host.get('estado') or {}).get('NOM_ESTADO', 'N/A')
            ctk.CTkLabel(self.details_frame, text=f"Estado: {estado}").pack(anchor="w", padx=10, pady=5)
        else:
            ctk.CTkLabel(self.details_frame, text="Error al cargar detalles del host.").pack(anchor="w", padx=10, pady=5)

    def load_monitoreo_data(self):
        # Clear previous plot/message
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        start_date = None
        end_date = None
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").isoformat()
            # Add one day to end_date to include the whole day
            end_date = (datetime.datetime.strptime(end_date_str, "%Y-%m-%d") + datetime.timedelta(days=1)).isoformat()
        except ValueError:
            error_label = ctk.CTkLabel(self.plot_frame, text="Formato de fecha inválido. Use YYYY-MM-DD.")
            error_label.pack(anchor="center", expand=True)
            return

        # Fetch monitoreo data from API
        monitoreo_data = self.api_client.get_monitoreo_by_host(self.host_id, start_date=start_date, end_date=end_date)
        if monitoreo_data:
            self.plot_monitoreo_data(monitoreo_data)
        else:
            no_data_label = ctk.CTkLabel(self.plot_frame, text="No hay datos de monitoreo disponibles para el rango de fechas seleccionado.")
            no_data_label.pack(anchor="center", expand=True)

    def plot_monitoreo_data(self, data):
        timestamps = [datetime.datetime.fromisoformat(d['TIMESTAMP']) for d in data]
        ping_results = [d['PING_RESULT'] for d in data]

        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        ax.plot(timestamps, ping_results, marker='o', linestyle='-')
        ax.set_title('Historial de Ping')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Resultado de Ping (ms)')
        ax.grid(True)
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()
