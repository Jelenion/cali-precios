import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import pandas as pd
from typing import Optional

# Configurar el modo de apariencia y tema de color predeterminado
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Definir los colores corporativos de Helados Cali
COLORES = {
    "primario": "#003B73",    # Azul corporativo
    "secundario": "#D61A1F",  # Rojo corporativo
    "acento": "#FFFFFF",      # Blanco para contraste
    "texto_claro": "#FFFFFF", # Blanco para texto sobre fondos oscuros
    "texto_oscuro": "#000000" # Negro para texto sobre fondos claros
}

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variables para guardar datos y archivo
        self.df: Optional[pd.DataFrame] = None
        self.archivo_excel: Optional[str] = None
        self.campos_a_actualizar = []

        # Configurar ventana principal
        self.title("Helados Cali - Sistema de Gestión")
        self.geometry("1000x600")

        # Configurar cuadrícula para dividir ventana
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Crear panel lateral y marco principal
        self.crear_panel_lateral()
        self.crear_marco_principal()

    def crear_panel_lateral(self):
        """Crea el panel lateral con botones y título"""
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            fg_color=COLORES["primario"],
            width=200,
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Título del menú lateral
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Menú Principal",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORES["texto_claro"]
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Botón para cargar Excel con selección previa
        self.btn_cargar_excel = ctk.CTkButton(
            self.sidebar_frame,
            text="Cargar Excel",
            fg_color=COLORES["secundario"],
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518",
            command=self.cargar_excel
        )
        self.btn_cargar_excel.grid(row=1, column=0, padx=20, pady=10)

        # Botón para mostrar datos cargados
        self.btn_mostrar_datos = ctk.CTkButton(
            self.sidebar_frame,
            text="Mostrar Datos",
            fg_color=COLORES["secundario"],
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518",
            command=self.mostrar_datos
        )
        self.btn_mostrar_datos.grid(row=2, column=0, padx=20, pady=10)

    def crear_marco_principal(self):
        """Marco principal con etiqueta y área de texto"""
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Etiqueta principal
        self.main_label = ctk.CTkLabel(
            self.main_frame,
            text="Sistema de Gestión de Productos",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORES["primario"]
        )
        self.main_label.pack(pady=30)

        # Área de texto para mostrar mensajes o datos
        self.text_area = ctk.CTkTextbox(
            self.main_frame,
            width=600,
            height=400,
            font=ctk.CTkFont(size=12),
            text_color=COLORES["texto_oscuro"],
            fg_color="#F5F5F5"
        )
        self.text_area.pack(pady=10, padx=10, fill="both", expand=True)

    def cargar_excel(self):
        """Muestra ventana para seleccionar campos a actualizar"""
        # Evitar abrir múltiples ventanas
        if hasattr(self, "ventana_seleccion") and self.ventana_seleccion.winfo_exists():
            self.ventana_seleccion.lift()
            self.ventana_seleccion.focus_force()
            return

        self.ventana_seleccion = ctk.CTkToplevel(self)
        ventana = self.ventana_seleccion
        ventana.title("Selecciona campos a actualizar")
        ventana.geometry("350x400")
        ventana.lift()
        ventana.attributes("-topmost", True)
        ventana.focus_force()
        ventana.grab_set()

        # Solo enlaza los eventos cuando la ventana secundaria está abierta
        self.main_frame.bind("<Button>", self.hacer_alerta_si_bloqueada)
        self.main_frame.bind("<Key>", self.hacer_alerta_si_bloqueada)
        self.bind("<FocusIn>", self.hacer_alerta_si_bloqueada)

        opciones = ["costAct", "costAnt", "costProm", "precioi1", "precioi2", "precioi3"]

        label = ctk.CTkLabel(ventana, text="Selecciona los campos a actualizar:", font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=10)

        self.check_vars = {}

        for campo in opciones:
            var = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(ventana, text=campo, variable=var)
            cb.pack(anchor="w", padx=20, pady=5)
            self.check_vars[campo] = var

        btn_confirmar = ctk.CTkButton(
            ventana, 
            text="Confirmar selección y cargar Excel", 
            command=lambda v=ventana: self.confirmar_campos_y_cargar(v)
        )
        btn_confirmar.pack(pady=20)

    def confirmar_campos_y_cargar(self, ventana_popup):
        """Carga el Excel tras confirmar selección de campos"""
        campos_seleccionados = [campo for campo, var in self.check_vars.items() if var.get()]

        if not campos_seleccionados:
            self.mostrar_mensaje("Error: Debes seleccionar al menos un campo para actualizar.")
            return

        ventana_popup.destroy()
        self.ventana_seleccion = None
        # Desenlaza los eventos cuando la ventana secundaria se cierra
        self.unbind("<FocusIn>")
        self.main_frame.unbind("<Button>")
        self.main_frame.unbind("<Key>")

        try:
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if filename:
                self.archivo_excel = filename
                self.df = pd.read_excel(filename)
                
                if 'codprod' not in self.df.columns:
                    self.mostrar_mensaje("Error: El archivo debe contener la columna 'codprod'")
                    self.df = None
                    return

                mensaje = f"Archivo cargado exitosamente.\nNombre: {filename}\n"
                mensaje += f"Campos seleccionados para actualizar: {', '.join(campos_seleccionados)}\n"
                mensaje += f"Columnas encontradas: {', '.join(self.df.columns)}\n"

                faltantes = [campo for campo in campos_seleccionados if campo not in self.df.columns]
                if faltantes:
                    mensaje += f"\nAdvertencia: Los siguientes campos no se encuentran en el archivo: {', '.join(faltantes)}"

                self.mostrar_mensaje(mensaje)

                self.campos_a_actualizar = campos_seleccionados

        except Exception as e:
            self.mostrar_mensaje(f"Error al cargar el archivo: {str(e)}")

    def mostrar_datos(self):
        """Muestra resumen y primeros 10 registros del Excel cargado"""
        if self.df is not None:
            info = f"Resumen del archivo:\n"
            info += f"Total de registros: {len(self.df)}\n"
            info += f"Columnas disponibles: {', '.join(self.df.columns)}\n\n"
            info += "Primeros 10 registros:\n"
            info += str(self.df.head(10))
            self.mostrar_mensaje(info)
        else:
            self.mostrar_mensaje("No hay datos cargados. Por favor, cargue un archivo Excel primero.")

    def mostrar_mensaje(self, mensaje: str):
        """Muestra un texto en el área principal"""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", mensaje)

    def hacer_alerta_si_bloqueada(self, event=None):
        """Emite un sonido de alerta si la ventana secundaria está abierta"""
        if hasattr(self, "ventana_seleccion") and self.ventana_seleccion is not None and self.ventana_seleccion.winfo_exists():
            self.bell()
            return "break"  # Evita que el evento siga propagándose
