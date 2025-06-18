import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
from typing import Optional
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.connection import conexion

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

CAMPOS_COSTOS = [
    ("costAct", "Costo Actual"),
    ("costprom", "Costo Promedio"),
    ("costant", "Costo Anterior")
]
CAMPOS_PRECIOS = [
    ("precio1", "Precio 1"),
    ("precio2", "Precio 2"),
    ("precio3", "Precio 3")
]

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variables para guardar datos y archivo
        self.df: Optional[pd.DataFrame] = None
        self.archivo_excel: Optional[str] = None
        self.campos_a_actualizar = []

        # Configurar ventana principal
        self.title("Helados Cali - Sistema de Gestión")
        self.geometry("1100x700")

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
            width=220,
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

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

        # Botón para seleccionar campos
        self.btn_seleccionar_campos = ctk.CTkButton(
            self.sidebar_frame,
            text="Seleccionar Campos",
            fg_color=COLORES["secundario"],
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518",
            command=self.abrir_seleccion_campos
        )
        self.btn_seleccionar_campos.grid(row=3, column=0, padx=20, pady=10)

        # Botón para actualizar
        self.btn_actualizar = ctk.CTkButton(
            self.sidebar_frame,
            text="Actualizar Base de Datos",
            fg_color=COLORES["secundario"],
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518",
            command=self.actualizar_base_datos
        )
        self.btn_actualizar.grid(row=4, column=0, padx=20, pady=10)

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
            width=700,
            height=500,
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

        opciones = ["CostAct", "CostAnt", "costProm", "PrecioIU1", "PrecioIU2", "PrecioIU3"]

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
                
                if 'CodProd' not in self.df.columns:
                    self.mostrar_mensaje("Error: El archivo debe contener la columna 'codprod'")
                    self.df = None
                    return
                
                # Verificar columnas recomendadas
                columnas_recomendadas = ['costAct', 'precio']
                columnas_faltantes = [col for col in columnas_recomendadas if col not in self.df.columns]
                
                mensaje = f"Archivo cargado exitosamente.\nNombre: {filename}\n"
                mensaje += f"Campos seleccionados para actualizar: {', '.join(campos_seleccionados)}\n"
                mensaje += f"Columnas encontradas: {', '.join(self.df.columns)}\n"
                
                if columnas_faltantes:
                    mensaje += f"\nAdvertencia: Columnas recomendadas faltantes: {', '.join(columnas_faltantes)}"
                
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

    def abrir_seleccion_campos(self):
        """Abre una ventana para seleccionar los campos a actualizar"""
        self.ventana_campos = ctk.CTkToplevel(self)
        self.ventana_campos.title("Seleccionar campos a actualizar")
        self.ventana_campos.geometry("400x400")

        ctk.CTkLabel(self.ventana_campos, text="Selecciona los campos de costos:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        self.vars_costos = {}
        for campo, label in CAMPOS_COSTOS:
            var = tk.BooleanVar()
            chk = ctk.CTkCheckBox(self.ventana_campos, text=label, variable=var)
            chk.pack(anchor="w", padx=30)
            self.vars_costos[campo] = var

        ctk.CTkLabel(self.ventana_campos, text="Selecciona los campos de precios:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        self.vars_precios = {}
        for campo, label in CAMPOS_PRECIOS:
            var = tk.BooleanVar()
            chk = ctk.CTkCheckBox(self.ventana_campos, text=label, variable=var)
            chk.pack(anchor="w", padx=30)
            self.vars_precios[campo] = var

        ctk.CTkButton(self.ventana_campos, text="Aceptar", command=self.guardar_campos_seleccionados).pack(pady=20)

    def guardar_campos_seleccionados(self):
        """Guarda los campos seleccionados por el usuario"""
        self.campos_seleccionados = []
        for campo, var in self.vars_costos.items():
            if var.get():
                self.campos_seleccionados.append(campo)
        for campo, var in self.vars_precios.items():
            if var.get():
                self.campos_seleccionados.append(campo)
        self.ventana_campos.destroy()
        self.mostrar_mensaje(f"Campos seleccionados: {', '.join(self.campos_seleccionados)}")

    def actualizar_base_datos(self):
        """Actualiza los registros en la base de datos según los campos seleccionados y el Excel cargado"""
        if self.df is None:
            self.mostrar_mensaje("Primero debe cargar un archivo Excel.")
            return
        if not self.campos_seleccionados:
            self.mostrar_mensaje("Debe seleccionar al menos un campo para actualizar.")
            return
        # Validar que las columnas seleccionadas existan en el Excel
        faltantes = [campo for campo in self.campos_seleccionados if campo not in self.df.columns]
        if faltantes:
            self.mostrar_mensaje(f"Faltan las siguientes columnas en el Excel: {', '.join(faltantes)}")
            return
        # Proceso de actualización
        resumen = []
        errores = []
        try:
            cursor = conexion.cursor()
            for idx, row in self.df.iterrows():
                codprod = row['codprod']
                set_clauses = []
                valores = []
                for campo in self.campos_seleccionados:
                    set_clauses.append(f"{campo} = ?")
                    valores.append(row[campo])
                if not set_clauses:
                    continue
                sql = f"UPDATE productos SET {', '.join(set_clauses)} WHERE codprod = ?"
                valores.append(codprod)
                try:
                    cursor.execute(sql, valores)
                    resumen.append(f"Registro {codprod} actualizado.")
                except Exception as e:
                    errores.append(f"Error en {codprod}: {str(e)}")
            conexion.commit()
            mensaje = f"Actualización completada.\nRegistros actualizados: {len(resumen)}\n"
            if errores:
                mensaje += f"Errores: {len(errores)}\n" + '\n'.join(errores[:10])
            else:
                mensaje += "Sin errores."
            self.mostrar_mensaje(mensaje)
        except Exception as e:
            self.mostrar_mensaje(f"Error general en la actualización: {str(e)}")

    def mostrar_mensaje(self, mensaje: str):
        """Muestra un texto en el área principal"""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", mensaje)

    def hacer_alerta_si_bloqueada(self, event=None):
        """Emite un sonido de alerta si la ventana secundaria está abierta"""
        if hasattr(self, "ventana_seleccion") and self.ventana_seleccion is not None and self.ventana_seleccion.winfo_exists():
            self.bell()
            return "break"  # Evita que el evento siga propagándose
