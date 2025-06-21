import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import pandas as pd
from typing import Optional
import os
from PIL import Image, ImageTk
from DB.connection import update_producto

# Configuración de colores corporativos
COLORES = {
    "primario": "#003B73",
    "secundario": "#D61A1F",
    "acento": "#FFFFFF",
    "texto_claro": "#FFFFFF",
    "texto_oscuro": "#000000",
    "fondo_tabla": "#f8f9fa",
    "fondo_encabezado": "#003B73",
    "texto_encabezado": "#FFFFFF",
    "fondo_principal": "#ffffff",
    "borde_suave": "#e9ecef"
}

# Campos que se pueden actualizar
CAMPOS_COSTOS = ["costact", "costprom", "costant"]
CAMPOS_PRECIOS = ["precio1", "precio2", "precio3"]
ARCHIVO_EXCEL = "datos.xlsx"

# Configuración de anchos fijos para columnas
ANCHOS_COLUMNAS = {
    "codprod": 180,
    "costact": 160,
    "costprom": 160,
    "costant": 160,
    "precio1": 160,
    "precio2": 160,
    "precio3": 160,
    "estado": 160,
    "detalle": 200
}

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.df: Optional[pd.DataFrame] = None
        self.campos_actualizables = []
        self.title("Helados Cali - Sistema de Gestión")
        self.geometry("1400x800")
        self.state('zoomed')  # Abrir siempre maximizada
        
        # Configurar grid principal con mejor distribución
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Para los logos
        self.grid_columnconfigure(1, weight=1)
        
        # Configurar tema y colores
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.crear_panel_lateral()
        self.crear_marco_principal()
        self.estilizar_treeview()
        self.cargar_excel_automatico()
        self.crear_logos_corporativos()

    def crear_logos_corporativos(self):
        """Crea los logos corporativos en las esquinas inferiores con mejor diseño."""
        # Frame principal para logos con mejor espaciado
        self.logos_frame = ctk.CTkFrame(
            self, 
            fg_color=COLORES["fondo_principal"], 
            height=100,
            corner_radius=0
        )
        self.logos_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        self.logos_frame.grid_columnconfigure(0, weight=1)
        self.logos_frame.grid_columnconfigure(1, weight=1)
        self.logos_frame.grid_rowconfigure(0, weight=1)
        
        # Frame interno para centrar los logos
        self.logos_inner_frame = ctk.CTkFrame(
            self.logos_frame,
            fg_color="transparent"
        )
        self.logos_inner_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=40, pady=15)
        self.logos_inner_frame.grid_columnconfigure(0, weight=1)
        self.logos_inner_frame.grid_columnconfigure(1, weight=1)
        
        # Logo izquierdo (corp.png) - optimizado para fondo transparente
        try:
            if os.path.exists("corp.png"):
                img_corp = Image.open("corp.png")
                # Convertir a RGBA si no lo está para manejar transparencia
                if img_corp.mode != 'RGBA':
                    img_corp = img_corp.convert('RGBA')
                
                # Redimensionar manteniendo proporción - tamaño más grande
                img_corp.thumbnail((150, 80), Image.Resampling.LANCZOS)
                self.photo_corp = ImageTk.PhotoImage(img_corp)
                
                # Label con fondo transparente
                self.logo_corp = tk.Label(
                    self.logos_inner_frame, 
                    image=self.photo_corp, 
                    bg=COLORES["fondo_principal"],
                    highlightthickness=0,
                    bd=0
                )
                self.logo_corp.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        except Exception as e:
            print(f"Error cargando corp.png: {e}")
        
        # Logo derecho (helados.png) - optimizado para fondo transparente
        try:
            if os.path.exists("helados.png"):
                img_helados = Image.open("helados.png")
                # Convertir a RGBA si no lo está para manejar transparencia
                if img_helados.mode != 'RGBA':
                    img_helados = img_helados.convert('RGBA')
                
                # Redimensionar manteniendo proporción - tamaño más grande
                img_helados.thumbnail((150, 80), Image.Resampling.LANCZOS)
                self.photo_helados = ImageTk.PhotoImage(img_helados)
                
                # Label con fondo transparente
                self.logo_helados = tk.Label(
                    self.logos_inner_frame, 
                    image=self.photo_helados, 
                    bg=COLORES["fondo_principal"],
                    highlightthickness=0,
                    bd=0
                )
                self.logo_helados.grid(row=0, column=1, padx=20, pady=5, sticky="e")
        except Exception as e:
            print(f"Error cargando helados.png: {e}")

    def crear_panel_lateral(self):
        """Crea el panel lateral con mejor diseño y espaciado."""
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            fg_color=COLORES["primario"], 
            width=250, 
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        
        # Título del panel lateral con mejor espaciado
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Sistema de Gestión",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLORES["texto_claro"]
        )
        self.logo_label.grid(row=0, column=0, padx=25, pady=(30, 20))
        
        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Helados Cali",
            font=ctk.CTkFont(size=20, weight="normal"),
            text_color=COLORES["texto_claro"]
        )
        self.subtitle_label.grid(row=1, column=0, padx=25, pady=(0, 30))
        
        # Botón de actualización con mejor diseño
        self.btn_actualizar = ctk.CTkButton(
            self.sidebar_frame, 
            text="🔄 Actualizar Base de Datos",
            fg_color=COLORES["secundario"], 
            text_color=COLORES["texto_claro"],
            hover_color="#AA1518", 
            command=self.actualizar_base_datos,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=8
        )
        self.btn_actualizar.grid(row=2, column=0, padx=25, pady=10)
        
        # Información adicional
        self.info_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="• Doble clic para editar\n",
            font=ctk.CTkFont(size=14),
            text_color=COLORES["texto_claro"],
            justify="left"
        )
        self.info_label.grid(row=3, column=0, padx=25, pady=20, sticky="w")

    def crear_marco_principal(self):
        """Crea el marco principal con mejor diseño y espaciado."""
        # Frame principal con mejor diseño
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color=COLORES["fondo_principal"],
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header con título y botón de recarga
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=80
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 0))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        
        # Título principal con mejor diseño
        self.main_label = ctk.CTkLabel(
            self.header_frame, 
            text="Gestión de Productos",
            font=ctk.CTkFont(size=40, weight="bold"), 
            text_color=COLORES["primario"]
        )
        self.main_label.grid(row=0, column=0, padx=0, pady=20, sticky="w")
        
        # Botón de recarga con mejor diseño
        self.btn_reload = ctk.CTkButton(
            self.header_frame,
            text="🔄",
            font=ctk.CTkFont(size=24, weight="bold"),
            command=self.recargar_excel,
            fg_color=COLORES["primario"],
            text_color=COLORES["texto_claro"],
            hover_color="#002a5a",
            width=60,
            height=60,
            corner_radius=30
        )
        self.btn_reload.grid(row=0, column=1, padx=(0, 10), pady=20)
        
        # Frame para la tabla con mejor diseño
        self.table_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORES["fondo_tabla"],
            corner_radius=12
        )
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar estilo de la tabla
        self.estilizar_treeview()
        
        # Crear tabla con mejor diseño
        self.tree = ttk.Treeview(self.table_frame, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Scrollbar con mejor diseño
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns", pady=15)
        
        # Binding para edición
        self.tree.bind('<Double-1>', self.editar_celda)

    def estilizar_treeview(self):
        """Estiliza la tabla con mejor diseño."""
        style = ttk.Style()
        style.theme_use("default")
        
        # Configurar estilo de la tabla
        style.configure(
            "Treeview",
            background=COLORES["fondo_tabla"],
            fieldbackground=COLORES["fondo_tabla"],
            font=("Segoe UI", 14),
            rowheight=40,
            borderwidth=0,
            relief="flat"
        )
        
        # Configurar encabezados
        style.configure(
            "Treeview.Heading",
            background=COLORES["fondo_encabezado"],
            foreground=COLORES["texto_encabezado"],
            font=("Segoe UI", 15, "bold"),
            borderwidth=0,
            relief="flat"
        )
        
        # Configurar selección
        style.map(
            "Treeview",
            background=[("selected", COLORES["primario"])],
            foreground=[("selected", COLORES["texto_claro"])]
        )

    def cargar_excel_automatico(self):
        """Carga automáticamente el archivo datos.xlsx al iniciar."""
        if not os.path.exists(ARCHIVO_EXCEL):
            messagebox.showerror("Error", f"No se encontró el archivo '{ARCHIVO_EXCEL}'. Colóquelo en la carpeta del programa.")
            self.btn_actualizar.configure(state="disabled")
            self.tree['columns'] = []
            return
        self.btn_actualizar.configure(state="normal")
        self.archivo_excel = ARCHIVO_EXCEL
        self.leer_y_mostrar_excel()

    def leer_y_mostrar_excel(self):
        """Lee y muestra los datos del Excel en la tabla."""
        try:
            self.df = pd.read_excel(self.archivo_excel)
            self.df.columns = [col.lower() for col in self.df.columns]
            if 'codprod' not in self.df.columns:
                messagebox.showerror("Error", "El archivo debe contener la columna 'codprod'.")
                self.df = None
                self.btn_actualizar.configure(state="disabled")
                return
            self.campos_actualizables = [col for col in self.df.columns if col in CAMPOS_COSTOS + CAMPOS_PRECIOS]
            if not self.campos_actualizables:
                messagebox.showwarning("Advertencia", "El archivo no contiene campos de costos ni precios actualizables.")
            self.mostrar_datos_en_tabla(self.df)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {str(e)}")
            self.df = None
            self.btn_actualizar.configure(state="disabled")

    def recargar_excel(self):
        """Recarga el Excel con efecto visual mejorado."""
        # Efecto de parpadeo profesional
        self.tree.grid_remove()
        self.update_idletasks()
        
        def mostrar_y_reaplicar():
            self.leer_y_mostrar_excel()
            self.tree.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
            self.aplicar_anchos_fijos()
        
        self.after(200, mostrar_y_reaplicar)

    def aplicar_anchos_fijos(self):
        """Aplica anchos fijos a todas las columnas visibles."""
        columnas_actuales = self.tree['columns']
        for col in columnas_actuales:
            ancho = ANCHOS_COLUMNAS.get(col, 160)
            self.tree.column(col, width=ancho, anchor="center", stretch=False)

    def mostrar_datos_en_tabla(self, df):
        """Muestra los datos en la tabla con mejor formato."""
        self.tree.delete(*self.tree.get_children())
        
        # Limpiar columnas previas
        for col in self.tree['columns']:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        
        columnas_a_mostrar = ['codprod'] + self.campos_actualizables
        self.tree['columns'] = columnas_a_mostrar
        
        # Configurar encabezados con mejor formato
        for col in columnas_a_mostrar:
            # Capitalizar y formatear nombres de columnas
            nombre_formateado = col.upper().replace('COST', 'COSTO ').replace('PRECIO', 'PRECIO ')
            self.tree.heading(col, text=nombre_formateado)
        
        # Insertar datos
        for idx, row in df.iterrows():
            values = [row.get(col, '') for col in columnas_a_mostrar]
            self.tree.insert('', 'end', iid=idx, values=values)
        
        # Aplicar anchos fijos
        self.aplicar_anchos_fijos()

    def editar_celda(self, event):
        """Permite editar una celda de la tabla con mejor diseño."""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or not column:
            return
        
        col_idx = int(column.replace('#', '')) - 1
        col_name = self.tree['columns'][col_idx]
        if col_name == 'codprod':
            return  # No permitir editar codprod
        
        x, y, width, height = self.tree.bbox(item, column)
        valor_actual = self.tree.set(item, col_name)
        
        # Entry con mejor diseño
        entry = tk.Entry(
            self.tree, 
            font=("Segoe UI", 14),
            bd=2,
            relief="solid",
            bg="white",
            fg=COLORES["texto_oscuro"]
        )
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, valor_actual)
        entry.select_range(0, tk.END)
        entry.focus()
        
        def guardar_edicion(event=None):
            nuevo_valor = entry.get()
            self.tree.set(item, col_name, nuevo_valor)
            self.df.at[int(item), col_name] = nuevo_valor
            entry.destroy()
        
        entry.bind('<Return>', guardar_edicion)
        entry.bind('<FocusOut>', lambda e: entry.destroy())

    def actualizar_base_datos(self):
        """Actualiza la base de datos y guarda los cambios en el Excel."""
        if self.df is None or not self.campos_actualizables:
            messagebox.showerror("Error", "Debe tener un archivo Excel válido con campos de costos o precios.")
            return
        
        # Mostrar progreso
        self.btn_actualizar.configure(text="⏳ Actualizando...", state="disabled")
        self.update_idletasks()
        
        resultados = []
        for idx, row in self.df.iterrows():
            codprod = row['codprod']
            campos_dict = {campo: row[campo] for campo in self.campos_actualizables if campo in row}
            exito, error = update_producto(codprod, campos_dict)
            if exito:
                resultados.append((codprod, "✅ Actualizado", ""))
            else:
                resultados.append((codprod, "❌ Error", error))
        
        # Guardar los cambios en el Excel
        try:
            self.df.to_excel(self.archivo_excel, index=False)
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo guardar el archivo Excel: {str(e)}")
        
        # Restaurar botón
        self.btn_actualizar.configure(text="🔄 Actualizar Base de Datos", state="normal")
        
        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        """Muestra los resultados con mejor formato."""
        self.tree.delete(*self.tree.get_children())
        
        # Limpiar columnas previas
        for col in self.tree['columns']:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        
        columnas_resultado = ["codprod", "estado", "detalle"]
        self.tree['columns'] = columnas_resultado
        
        # Configurar encabezados
        headers = {"codprod": "CÓDIGO", "estado": "ESTADO", "detalle": "DETALLE"}
        for col in columnas_resultado:
            self.tree.heading(col, text=headers.get(col, col.upper()))
        
        # Insertar resultados
        for codprod, estado, detalle in resultados:
            self.tree.insert('', 'end', values=(codprod, estado, detalle))
        
        # Aplicar anchos fijos
        self.aplicar_anchos_fijos()
