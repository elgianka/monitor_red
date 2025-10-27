import customtkinter as ctk
from api_client import ApiClient
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.inventory_view import InventoryView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Monitoreo Conectividad AGK")
        self.geometry("1280x720") # Increased window size
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # Configure content area column

        self.api_client = ApiClient()
        self.current_view = None

        # Show login view initially
        self.login_view = LoginView(self, api_client=self.api_client, on_login_success=self.on_login_success)
        self.login_view.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def on_login_success(self):
        self.login_view.destroy()
        self.setup_main_ui()

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

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Initialize views
        self.views = {
            "dashboard": DashboardView(self.main_frame, api_client=self.api_client),
            "inventory": InventoryView(self.main_frame, api_client=self.api_client)
        }

        # Select default view
        self.select_view("dashboard")

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
