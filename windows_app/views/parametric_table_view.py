import customtkinter as ctk
from tkinter import messagebox
from api_client import ApiClient
from CTkTable import CTkTable

class ParametricItemDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, fields, initial_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.fields = fields
        self.entries = {}

        self.grid_columnconfigure(1, weight=1)

        row = 0
        # Get the name of the ID field
        id_field_name = list(self.fields.keys())[0]

        for field_name, field_info in fields.items():
            if field_name == id_field_name and not initial_data: # ID is usually auto-generated or not editable on creation
                continue
            
            label_text = field_info.get("label", field_name)
            field_type = field_info.get("type", "text")

            label = ctk.CTkLabel(self, text=f"{label_text}:")
            label.grid(row=row, column=0, padx=20, pady=5, sticky="w")

            if field_name == id_field_name:
                entry = ctk.CTkLabel(self, text=str(initial_data.get(field_name, "")))
                entry.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
            else:
                if field_type == "text":
                    entry = ctk.CTkEntry(self, width=250)
                    entry.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
                    self.entries[field_name] = entry
                # Add more field types here if needed (e.g., combobox for foreign keys, date picker)
            
            if initial_data and field_name in self.entries:
                self.entries[field_name].insert(0, str(initial_data.get(field_name, "")))
            row += 1

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=row, column=0, columnspan=2, padx=20, pady=20, sticky="e")

        self.save_button = ctk.CTkButton(self.buttons_frame, text="Guardar", command=self._on_save)
        self.save_button.pack(side="left", padx=(0, 10))

        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancelar", fg_color="#555555", command=self._on_cancel)
        self.cancel_button.pack(side="left")

        self.wait_window()

    def _on_save(self):
        data = {}
        for field_name, entry in self.entries.items():
            data[field_name] = entry.get()
        self.result = data
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def get_input(self):
        return self.result

class ParametricTableView(ctk.CTkFrame):
    def __init__(self, parent, api_client: ApiClient, endpoint: str, title: str, fields: dict):
        super().__init__(parent)
        self.api_client = api_client
        self.endpoint = endpoint
        self.title = title
        self.fields = fields
        self.selected_row_index = None # To store the selected row

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title and Buttons Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header_frame, text=self.title, font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.buttons_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=1, sticky="e")

        self.add_button = ctk.CTkButton(self.buttons_frame, text="Añadir", command=self._add_item)
        self.add_button.pack(side="left", padx=(0, 10))

        self.edit_button = ctk.CTkButton(self.buttons_frame, text="Editar", command=self._edit_item, state="disabled")
        self.edit_button.pack(side="left", padx=(0, 10))

        self.delete_button = ctk.CTkButton(self.buttons_frame, text="Eliminar", command=self._delete_item, state="disabled")
        self.delete_button.pack(side="left")
        
        self.refresh_button = ctk.CTkButton(self.buttons_frame, text="Refrescar", command=self.load_items)
        self.refresh_button.pack(side="left", padx=(10, 0))

        # Table for displaying items
        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.table = None
        self.load_items()

    def load_items(self):
        # Reset selection on load
        self.selected_row_index = None
        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

        if self.table:
            self.table.destroy()

        public_endpoints = ["sedes", "categorias", "estados", "marcas", "modelos", "procesos", "responsables", "ubicaciones"]
        
        items = None
        if self.endpoint in public_endpoints:
            # Dynamically call the correct public method, e.g., get_sedes(), get_categorias()
            method_to_call = getattr(self.api_client, f"get_{self.endpoint}", None)
            if method_to_call:
                items = method_to_call()
            else:
                # Fallback or error for safety, though it shouldn't be reached with the current structure
                items = self.api_client._get_public_items(self.endpoint)
        else:
            items = self.api_client.get_all_items(self.endpoint)

        if items is None:
            messagebox.showerror("Error", f"No se pudieron cargar los {self.endpoint}.")
            items = []

        # Prepare table data
        header = [info["label"] for info in self.fields.values()]
        
        self.item_map = {i: item for i, item in enumerate(items)}
        
        table_data = [header]
        for item in items:
            row = [item.get(key, "") for key in self.fields.keys()]
            table_data.append(row)

        if len(table_data) > 1:
            self.table = CTkTable(self.table_frame, values=table_data, command=self._on_table_click)
            self.table.pack(expand=True, fill="both")
        else:
            no_data_label = ctk.CTkLabel(self.table_frame, text=f"No hay {self.endpoint} para mostrar.")
            no_data_label.pack(pady=20)

    def _on_table_click(self, data):
        self.selected_row_index = data["row"]
        # Enable edit/delete buttons if a data row is clicked
        if self.selected_row_index > 0:
            self.edit_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else: # Disable if header is clicked
            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def _get_selected_item_data(self):
        if self.selected_row_index is None or self.selected_row_index == 0:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un elemento de la tabla.")
            return None, None
        
        # The first row (index 0) is the header, so data rows start at index 1.
        # The item_map is 0-indexed. So, table row 1 corresponds to item_map index 0.
        item_index = self.selected_row_index - 1
        
        if item_index in self.item_map:
            item_data = self.item_map[item_index]
            id_field_name = list(self.fields.keys())[0]
            item_id = item_data.get(id_field_name)
            return item_id, item_data
        
        messagebox.showerror("Error", "No se pudo encontrar el elemento seleccionado.")
        return None, None

    def _add_item(self):
        # Deselect row before adding
        self.selected_row_index = None
        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

        dialog = ParametricItemDialog(self, f"Añadir {self.title.lower().replace('gestión de ', '')}", self.fields)
        data = dialog.get_input()
        if data:
            response = self.api_client.create_item(self.endpoint, data)
            if response:
                messagebox.showinfo("Éxito", f"{self.title.replace('Gestión de ', '')} añadido correctamente.")
                self.load_items()
            else:
                messagebox.showerror("Error", f"No se pudo añadir el {self.title.lower().replace('gestión de ', '')}.")

    def _edit_item(self):
        item_id, current_data = self._get_selected_item_data()
        if not item_id:
            return

        dialog = ParametricItemDialog(self, f"Editar {self.title.lower().replace('gestión de ', '')}", self.fields, initial_data=current_data)
        updated_data = dialog.get_input()

        if updated_data:
            response = self.api_client.update_item(self.endpoint, item_id, updated_data)
            if response:
                messagebox.showinfo("Éxito", f"{self.title.replace('Gestión de ', '')} actualizado correctamente.")
                self.load_items()
            else:
                messagebox.showerror("Error", f"No se pudo actualizar el {self.title.lower().replace('gestión de ', '')}.")

    def _delete_item(self):
        item_id, _ = self._get_selected_item_data()
        if not item_id:
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este elemento?"):
            response = self.api_client.delete_item(self.endpoint, item_id)
            if response:
                messagebox.showinfo("Éxito", f"{self.title.replace('Gestión de ', '')} eliminado correctamente.")
                self.load_items()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el {self.title.lower().replace('gestión de ', '')}.")