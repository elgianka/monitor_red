import customtkinter as ctk
from tkinter import messagebox
from views.edit_host_dialog import EditHostDialog
from views.add_host_dialog import AddHostDialog

class InventoryView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.api_client = api_client

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Gestión de Inventario", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=1, sticky="e")

        self.add_host_button = ctk.CTkButton(self.buttons_frame, text="Añadir Host", command=self.add_host)
        self.add_host_button.pack(side="left", padx=(0, 10))

        self.refresh_button = ctk.CTkButton(self.buttons_frame, text="Refrescar", command=self.load_hosts)
        self.refresh_button.pack(side="left")

        # Hosts Table
        self.hosts_frame = ctk.CTkScrollableFrame(self)
        self.hosts_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")

        self.load_hosts()

    def load_hosts(self):
        for widget in self.hosts_frame.winfo_children():
            widget.destroy()
        loading_label = ctk.CTkLabel(self.hosts_frame, text="Cargando hosts...")
        loading_label.pack(pady=20)

        try:
            hosts = self.api_client.get_hosts()
            loading_label.destroy()
            if hosts:
                self.create_table_header()
                for i, host in enumerate(hosts):
                    self.add_host_to_table(i, host)
            else:
                ctk.CTkLabel(self.hosts_frame, text="No se encontraron hosts.").pack(pady=20)
        except Exception as e:
            loading_label.destroy()
            ctk.CTkLabel(self.hosts_frame, text=f"Error al cargar hosts: {e}").pack(pady=20)

    def create_table_header(self):
        header_frame = ctk.CTkFrame(self.hosts_frame, fg_color="#333333")
        header_frame.pack(fill="x", expand=True, padx=10, pady=5)
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        headers = ["Nombre", "Dirección IP", "Estado", "Acciones"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=10, pady=10)

    def add_host_to_table(self, index, host):
        row_frame = ctk.CTkFrame(self.hosts_frame, fg_color=["#E5E5E5", "#2B2B2B"] if index % 2 == 0 else ["#F2F2F2", "#222222"])
        row_frame.pack(fill="x", expand=True, padx=10, pady=2)
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        ctk.CTkLabel(row_frame, text=host.get("H_NOM", "N/A")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(row_frame, text=host.get("H_IP", "N/A")).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(row_frame, text=host.get("estado", {}).get("E_NOM", "N/A")).grid(row=0, column=2, padx=10, pady=5)
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=3, padx=10, pady=5)
        edit_button = ctk.CTkButton(actions_frame, text="Editar", width=70, command=lambda h=host: self.edit_host(h))
        edit_button.pack(side="left", padx=5)
        delete_button = ctk.CTkButton(actions_frame, text="Eliminar", width=70, fg_color="#C00000", hover_color="#990000", command=lambda h=host: self.delete_host(h))
        delete_button.pack(side="left", padx=5)

    def add_host(self):
        dialog = AddHostDialog(self)
        host_data = dialog.get_input()
        if host_data:
            try:
                new_host = self.api_client.create_host(host_data)
                if new_host:
                    self.load_hosts()
                else:
                    messagebox.showerror("Error", "No se pudo crear el host.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear el host: {e}")

    def edit_host(self, host):
        dialog = EditHostDialog(self, host_data=host)
        updated_data = dialog.get_input()
        if updated_data:
            try:
                success = self.api_client.update_host(host.get("H_ID"), updated_data)
                if success:
                    self.load_hosts()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el host.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar el host: {e}")

    def delete_host(self, host):
        host_name = host.get("H_NOM", "N/A")
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el host '{host_name}'?"):
            try:
                success = self.api_client.delete_host(host.get("H_ID"))
                if success:
                    self.load_hosts()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el host.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el host: {e}")
