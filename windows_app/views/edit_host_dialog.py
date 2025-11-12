import customtkinter as ctk
from tkinter import messagebox
from api_client import ApiClient
import datetime

class EditHostDialog(ctk.CTkToplevel):
    def __init__(self, parent, api_client: ApiClient, host_data: dict):
        super().__init__(parent)

        self.title("Editar Host")
        self.geometry("600x700") # Increased size for more fields
        self.transient(parent) # Keep window on top
        self.grab_set() # Modal behavior

        self.api_client = api_client
        self.host_data = host_data
        self.result = None
        self.widgets = {}
        self.combobox_data = {}

        self.grid_columnconfigure(1, weight=1)

        self._load_combobox_data()
        self._create_widgets()
        self._prefill_widgets()

        self.wait_window()

    def _load_combobox_data(self):
        self.combobox_data["modelos"] = self.api_client.get_modelos() or []
        self.combobox_data["responsables"] = self.api_client.get_responsables() or []
        self.combobox_data["ubicaciones"] = self.api_client.get_ubicaciones() or []
        self.combobox_data["procesos"] = self.api_client.get_procesos() or []
        self.combobox_data["categorias"] = self.api_client.get_categorias() or []
        self.combobox_data["estados"] = self.api_client.get_estados() or []
        self.combobox_data["sedes"] = self.api_client.get_sedes() or []

    def _create_widgets(self):
        row = 0

        # NOM_HOST
        self._create_label_entry(row, "Nombre:", "NOM_HOST")
        row += 1

        # IP_HOST
        self._create_label_entry(row, "Dirección IP:", "IP_HOST")
        row += 1

        # MAC_HOST
        self._create_label_entry(row, "MAC:", "MAC_HOST")
        row += 1

        # NUM_SERIE
        self._create_label_entry(row, "Número de Serie:", "NUM_SERIE")
        row += 1

        # FIRMWARE_VERSION
        self._create_label_entry(row, "Versión Firmware:", "FIRMWARE_VERSION")
        row += 1

        # FECHA_ALTA
        self._create_label_entry(row, "Fecha de Alta (YYYY-MM-DD):", "FECHA_ALTA")
        row += 1

        # ANHO_ALTA
        self._create_label_entry(row, "Año de Alta:", "ANHO_ALTA")
        row += 1

        # LIM_SUP_PING
        self._create_label_entry(row, "Límite Superior Ping:", "LIM_SUP_PING")
        row += 1

        # LIM_INF_PING
        self._create_label_entry(row, "Límite Inferior Ping:", "LIM_INF_PING")
        row += 1

        # ID_MODELO
        self._create_label_combobox(row, "Modelo:", "ID_MODELO", self.combobox_data["modelos"], "ID_MODELO", "NOM_MODELO")
        row += 1

        # ID_RESPONSABLE
        self._create_label_combobox(row, "Responsable:", "ID_RESPONSABLE", self.combobox_data["responsables"], "ID_RESPONSABLE", "NOM_RESPONSABLE")
        row += 1

        # ID_UBICACION
        self._create_label_combobox(row, "Ubicación:", "ID_UBICACION", self.combobox_data["ubicaciones"], "ID_UBICACION", "NOM_UBICACION")
        row += 1

        # ID_PROCESO
        self._create_label_combobox(row, "Proceso:", "ID_PROCESO", self.combobox_data["procesos"], "ID_PROCESO", "NOM_PROCESO")
        row += 1

        # ID_CATEGORIA
        self._create_label_combobox(row, "Categoría:", "ID_CATEGORIA", self.combobox_data["categorias"], "ID_CATEGORIA", "NOM_CATEGORIA")
        row += 1

        # ID_ESTADO
        self._create_label_combobox(row, "Estado:", "ID_ESTADO", self.combobox_data["estados"], "ID_ESTADO", "NOM_ESTADO")
        row += 1

        # ID_SEDE
        self._create_label_combobox(row, "Sede:", "ID_SEDE", self.combobox_data["sedes"], "ID_SEDE", "NOM_SEDE")
        row += 1

        # --- Buttons ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=row, column=0, columnspan=2, padx=20, pady=20, sticky="e")

        self.save_button = ctk.CTkButton(self.buttons_frame, text="Guardar", command=self._on_save)
        self.save_button.pack(side="left", padx=(0, 10))

        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancelar", fg_color="#555555", command=self._on_cancel)
        self.cancel_button.pack(side="left")

    def _create_label_entry(self, row, label_text, field_name, initial_value=""):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=20, pady=5, sticky="w")
        entry = ctk.CTkEntry(self, width=250)
        entry.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
        self.widgets[field_name] = entry

    def _create_label_combobox(self, row, label_text, field_name, options_data, id_key, name_key):
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=20, pady=5, sticky="w")

        display_options = [item[name_key] for item in options_data] if options_data else []
        combobox = ctk.CTkComboBox(self, values=display_options, state="readonly")
        combobox.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
        self.widgets[field_name] = combobox
        self.widgets[f"{field_name}_map"] = {item[name_key]: item[id_key] for item in options_data} if options_data else {}

    def _prefill_widgets(self):
        for field_name, widget in self.widgets.items():
            if field_name.endswith("_map"): continue

            value = self.host_data.get(field_name)
            if value is not None:
                if isinstance(widget, ctk.CTkEntry):
                    if field_name == "FECHA_ALTA" and isinstance(value, str):
                        # Assuming FECHA_ALTA comes as a string in YYYY-MM-DD format
                        widget.insert(0, value)
                    else:
                        widget.insert(0, str(value))
                elif isinstance(widget, ctk.CTkComboBox):
                    id_map = self.widgets.get(f"{field_name}_map", {})
                    # Find the name corresponding to the ID
                    name_to_set = next((name for name, item_id in id_map.items() if item_id == value), "")
                    if name_to_set:
                        widget.set(name_to_set)

    def _on_save(self):
        data = {}
        for field_name, widget in self.widgets.items():
            if isinstance(widget, ctk.CTkEntry):
                value = widget.get()
                if value:
                    # Type conversion based on expected model types
                    if field_name in ["ANHO_ALTA"]:
                        try: data[field_name] = int(value)
                        except ValueError: data[field_name] = None
                    elif field_name in ["LIM_SUP_PING", "LIM_INF_PING"]:
                        try: data[field_name] = float(value)
                        except ValueError: data[field_name] = None
                    elif field_name == "FECHA_ALTA":
                        try: data[field_name] = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                        except ValueError: data[field_name] = None
                    else:
                        data[field_name] = value
                else:
                    data[field_name] = None
            elif isinstance(widget, ctk.CTkComboBox):
                selected_name = widget.get()
                id_map = self.widgets.get(f"{field_name}_map", {})
                data[field_name] = id_map.get(selected_name)

        # Basic validation for required fields
        if not data.get("NOM_HOST") or not data.get("IP_HOST"):
            messagebox.showerror("Error de Validación", "Nombre del Host y Dirección IP son obligatorios.")
            return

        self.result = data
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def get_input(self):
        return self.result
