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

        # Variables de clase
        self.df: Optional[pd.DataFrame] = None
        self.archivo_excel: Optional[str] = None

        # Configurar ventana
        self.title("Helados Cali - Sistema de Gestión")
        self.geometry("1000x600")

        # Configurar diseño de cuadrícula
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Crear panel lateral con widgets
        self.crear_panel_lateral()
        
        # Crear marco principal
        self.crear_marco_principal()

    def crear_panel_lateral(self):
        """Crea el panel lateral con sus botones y elementos"""
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            fg_color=COLORES["primario"],
            width=200,
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Título del menú
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Menú Principal",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORES["texto_claro"]
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Botón para cargar Excel
        self.btn_cargar_excel = ctk.CTkButton(
            self.sidebar_frame,
            text="Cargar Excel",
            fg_color=COLORES["secundario"],
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518",  # Rojo más oscuro para hover
            command=self.cargar_excel
        )
        self.btn_cargar_excel.grid(row=1, column=0, padx=20, pady=10)

        # Botón para mostrar datos
        self.btn_mostrar_datos = ctk.CTkButton(
            self.sidebar_frame,
            text="Mostrar Datos",
            fg_color=COLORES["secundario"],
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518",  # Rojo más oscuro para hover
            command=self.mostrar_datos
        )
        self.btn_mostrar_datos.grid(row=2, column=0, padx=20, pady=10)

    def crear_marco_principal(self):
        """Crea el marco principal y sus elementos"""
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Etiqueta de bienvenida
        self.main_label = ctk.CTkLabel(
            self.main_frame,
            text="Sistema de Gestión de Productos",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORES["primario"]
        )
        self.main_label.pack(pady=30)

        # Área de texto para mostrar información
        self.text_area = ctk.CTkTextbox(
            self.main_frame,
            width=600,
            height=400,
            font=ctk.CTkFont(size=12),
            text_color=COLORES["texto_oscuro"],
            fg_color="#F5F5F5"  # Fondo gris claro para el área de texto
        )
        self.text_area.pack(pady=10, padx=10, fill="both", expand=True)

    def cargar_excel(self):
        """Maneja la carga del archivo Excel"""
        try:
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if filename:
                self.archivo_excel = filename
                self.df = pd.read_excel(filename)
                
                # Verificar columna requerida
                if 'codprod' not in self.df.columns:
                    self.mostrar_mensaje("Error: El archivo debe contener la columna 'codprod'")
                    self.df = None
                    return
                
                # Verificar columnas recomendadas
                columnas_recomendadas = ['costAct', 'precio']
                columnas_faltantes = [col for col in columnas_recomendadas if col not in self.df.columns]
                
                mensaje = f"Archivo cargado exitosamente.\nNombre: {filename}\n"
                mensaje += f"Columnas encontradas: {', '.join(self.df.columns)}\n"
                
                if columnas_faltantes:
                    mensaje += f"\nAdvertencia: Columnas recomendadas faltantes: {', '.join(columnas_faltantes)}"
                
                self.mostrar_mensaje(mensaje)
        
        except Exception as e:
            self.mostrar_mensaje(f"Error al cargar el archivo: {str(e)}")

    def mostrar_datos(self):
        """Muestra los datos del Excel en el área de texto"""
        if self.df is not None:
            # Mostrar información básica
            info = f"Resumen del archivo:\n"
            info += f"Total de registros: {len(self.df)}\n"
            info += f"Columnas disponibles: {', '.join(self.df.columns)}\n\n"
            
            # Mostrar primeros 10 registros
            info += "Primeros 10 registros:\n"
            info += str(self.df.head(10))
            
            self.mostrar_mensaje(info)
        else:
            self.mostrar_mensaje("No hay datos cargados. Por favor, cargue un archivo Excel primero.")

    def mostrar_mensaje(self, mensaje: str):
        """Muestra un mensaje en el área de texto"""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", mensaje) 