import customtkinter as ctk

class AddHostDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Añadir Host")
        self.geometry("400x300")
        self.transient(parent) # Keep window on top
        self.grab_set() # Modal behavior

        self.result = None

        self.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        self.name_label = ctk.CTkLabel(self, text="Nombre:")
        self.name_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.name_entry = ctk.CTkEntry(self, width=250)
        self.name_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        self.ip_label = ctk.CTkLabel(self, text="Dirección IP:")
        self.ip_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.ip_entry = ctk.CTkEntry(self, width=250)
        self.ip_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # --- Buttons ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="e")

        self.add_button = ctk.CTkButton(self.buttons_frame, text="Añadir", command=self.add)
        self.add_button.pack(side="left", padx=(0, 10))

        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancelar", fg_color="#555555", command=self.cancel)
        self.cancel_button.pack(side="left")

        self.wait_window()

    def add(self):
        self.result = {
            "H_NOM": self.name_entry.get(),
            "H_IP": self.ip_entry.get(),
            "H_ID_ESTADO": 1 # Default state ID
        }
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def get_input(self):
        return self.result
