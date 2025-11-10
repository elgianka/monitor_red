import customtkinter as ctk
from api_client import ApiClient
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.inventory_view import InventoryView
from views.parametric_table_view import ParametricTableView
from monitoring_service import MonitoringService

class ParametricConfigView(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent)
        self.app_instance = app_instance
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Configuración de Tablas Paramétricas", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        parametric_tables = {
            "Marcas": "marcas",
            "Modelos": "modelos",
            "Áreas": "areas",
            "Sedes": "sedes",
            "Gerencias": "gerencias",
            "Estados": "estados",
            "Categorías": "categorias",
            "Procesos": "procesos",
            "Ubicaciones": "ubicaciones", # Assuming 'ubicaciones' is also a parametric table
            "Responsables": "responsables" # Assuming 'responsables' is also a parametric table
        }

        row = 0
        for display_name, endpoint_name in parametric_tables.items():
            button = ctk.CTkButton(self.buttons_frame, text=f"Gestión de {display_name}",
                                   command=lambda ep=endpoint_name: self.app_instance.select_view(f"parametric_{ep}"))
            button.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            row += 1

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Monitoreo Conectividad AGK")
        self.geometry("1280x720") # Increased window size
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # Configure content area column

        self.api_client = ApiClient()
        self.current_view = None
        self.monitoring_service = None
        self.views = {}
        self.ui_refresh_interval = 1000 # Refresh UI every 1000ms (1 second)

        self.login_view = LoginView(self, api_client=self.api_client, on_login_success=self.on_login_success)
        self.login_view.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_login_success(self):
        self.login_view.destroy()
        self.setup_main_ui()
        # Start monitoring service
        self.monitoring_service = MonitoringService(self.api_client)
        self.monitoring_service.start()
        self.start_ui_refresh() # Start UI refresh after monitoring service starts

    def on_closing(self):
        if self.monitoring_service:
            self.monitoring_service.stop()
        self.destroy()

    def setup_main_ui(self):
        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Monitoreo AGK  ",
                                                   font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = ctk.CTkButton(self.navigation_frame, text="Dashboard",
                                              command=lambda: self.select_view("dashboard"))
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.inventory_button = ctk.CTkButton(self.navigation_frame, text="Inventario",
                                              command=lambda: self.select_view("inventory"))
        self.inventory_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.config_button = ctk.CTkButton(self.navigation_frame, text="Configuración",
                                              command=lambda: self.select_view("parametric_config"))
        self.config_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Initialize views
        self.views = {
            "dashboard": DashboardView(self.main_frame, api_client=self.api_client, monitoring_service=self.monitoring_service), # Pass monitoring_service
            "inventory": InventoryView(self.main_frame, api_client=self.api_client),
            "parametric_config": ParametricConfigView(self.main_frame, self), # New config view

            # Parametric Table Views
            "parametric_marcas": ParametricTableView(
                self.main_frame, self.api_client, "marcas", "Gestión de Marcas",
                {"ID_MARCA": {"label": "ID", "width": 50}, "NOM_MARCA": {"label": "Nombre", "width": 200}}
            ),
            "parametric_modelos": ParametricTableView(
                self.main_frame, self.api_client, "modelos", "Gestión de Modelos",
                {"ID_MODELO": {"label": "ID", "width": 50}, "NOM_MODELO": {"label": "Nombre", "width": 200}, "ID_MARCA": {"label": "ID Marca", "width": 100}}
            ),
            "parametric_areas": ParametricTableView(
                self.main_frame, self.api_client, "areas", "Gestión de Áreas",
                {"ID_AREA": {"label": "ID", "width": 50}, "NOM_AREA": {"label": "Nombre", "width": 200}}
            ),
            "parametric_sedes": ParametricTableView(
                self.main_frame, self.api_client, "sedes", "Gestión de Sedes",
                {"ID_SEDE": {"label": "ID", "width": 50}, "NOM_SEDE": {"label": "Nombre", "width": 200}}
            ),
            "parametric_gerencias": ParametricTableView(
                self.main_frame, self.api_client, "gerencias", "Gestión de Gerencias",
                {"ID_GERENCIA": {"label": "ID", "width": 50}, "NOM_GERENCIA": {"label": "Nombre", "width": 200}}
            ),
            "parametric_estados": ParametricTableView(
                self.main_frame, self.api_client, "estados", "Gestión de Estados",
                {"ID_ESTADO": {"label": "ID", "width": 50}, "NOM_ESTADO": {"label": "Nombre", "width": 200}}
            ),
            "parametric_categorias": ParametricTableView(
                self.main_frame, self.api_client, "categorias", "Gestión de Categorías",
                {"ID_CATEGORIA": {"label": "ID", "width": 50}, "NOM_CATEGORIA": {"label": "Nombre", "width": 200}}
            ),
            "parametric_procesos": ParametricTableView(
                self.main_frame, self.api_client, "procesos", "Gestión de Procesos",
                {"ID_PROCESO": {"label": "ID", "width": 50}, "NOM_PROCESO": {"label": "Nombre", "width": 200}}
            ),
            "parametric_ubicaciones": ParametricTableView(
                self.main_frame, self.api_client, "ubicaciones", "Gestión de Ubicaciones",
                {"ID_UBICACION": {"label": "ID", "width": 50}, "NOM_UBICACION": {"label": "Nombre", "width": 200}, "ID_SEDE": {"label": "ID Sede", "width": 100}}
            ),
            "parametric_responsables": ParametricTableView(
                self.main_frame, self.api_client, "responsables", "Gestión de Responsables",
                {"ID_RESPONSABLE": {"label": "ID", "width": 50}, "NOM_RESPONSABLE": {"label": "Nombre", "width": 150}, "ID_AREA": {"label": "ID Area", "width": 100}}
            ),
        }

        # Select default view
        self.select_view("dashboard")

    def start_ui_refresh(self):
        self.after(self.ui_refresh_interval, self.refresh_dashboard_ui)

    def refresh_dashboard_ui(self):
        if self.current_view == self.views["dashboard"] and self.monitoring_service:
            # Pass the realtime_ping_results to the dashboard view
            self.views["dashboard"].update_dashboard(self.monitoring_service.realtime_ping_results)
        self.after(self.ui_refresh_interval, self.refresh_dashboard_ui)

    def select_view(self, name):
        # Hide current view if it exists
        if self.current_view:
            self.current_view.grid_forget()

        # Show the selected view
        self.current_view = self.views[name]
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
