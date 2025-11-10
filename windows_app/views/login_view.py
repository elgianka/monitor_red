import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, api_client, on_login_success):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.api_client = api_client
        self.on_login_success = on_login_success

        # Center the login form
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=30, pady=30)

        self.title_label = ctk.CTkLabel(self.form_frame, text="Iniciar Sesión", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=50, pady=(30, 20))

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Usuario", width=250)
        self.username_entry.grid(row=1, column=0, columnspan=2, padx=50, pady=10)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Contraseña", show="*", width=250)
        self.password_entry.grid(row=2, column=0, columnspan=2, padx=50, pady=10)

        self.login_button = ctk.CTkButton(self.form_frame, text="Ingresar", command=self.login, width=250)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=50, pady=20)

        self.error_label = ctk.CTkLabel(self.form_frame, text="", text_color="#ff4d4d")
        self.error_label.grid(row=4, column=0, columnspan=2, padx=50, pady=(0, 30))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Usuario y contraseña son requeridos.")
            return

        self.login_button.configure(state="disabled", text="Ingresando...")
        self.update_idletasks() # Force UI update to show disabled state

        try:
            authenticated, error_msg = self.api_client.authenticate(username, password)
        except Exception as e:
            authenticated = False
            error_msg = str(e)
            print(f"Login exception: {e}")

        self.login_button.configure(state="normal", text="Ingresar")

        if authenticated:
            self.on_login_success()
        else:
            error_text = "Error de autenticación. Verifique sus credenciales."
            if error_msg:
                error_text = f"Error de autenticación: {error_msg}"
            self.error_label.configure(text=error_text)
