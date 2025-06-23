import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import pandas as pd
import pyodbc
from typing import Optional
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

COLORES = {
    "primario": "#2D3250",           # Azul oscuro elegante
    "secundario": "#424769",         # Azul grisáceo
    "acento": "#676F9D",            # Azul medio
    "acento_claro": "#7C85B3",      # Azul claro
    "fondo": "#F5F5F7",             # Gris muy claro
    "fondo_tabla": "#FFFFFF",       # Blanco puro
    "texto_claro": "#FFFFFF",       # Blanco
    "texto_oscuro": "#2D3250",      # Azul oscuro
    "borde": "#E5E5E7",            # Gris claro para bordes
    "hover": "#535878"             # Color hover para botones
}

def configurar_estilo_tabla():
    style = ttk.Style()
    style.theme_use('default')
    
    # Configurar el estilo de la tabla
    style.configure(
        "Custom.Treeview",
        background=COLORES["fondo_tabla"],
        foreground=COLORES["texto_oscuro"],
        fieldbackground=COLORES["fondo_tabla"],
        borderwidth=0,
        rowheight=30
    )
    
    # Configurar el estilo de los encabezados
    style.configure(
        "Custom.Treeview.Heading",
        background=COLORES["secundario"],
        foreground=COLORES["texto_claro"],
        borderwidth=1,
        relief="flat",
        font=('Segoe UI', 10, 'bold')
    )
    
    # Configurar selección
    style.map(
        "Custom.Treeview",
        background=[('selected', COLORES["acento"])],
        foreground=[('selected', COLORES["texto_claro"])]
    )

def obtener_conexion():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=192.168.0.106;'
            'DATABASE=hcdb2;'
            'UID=sa;'
            'PWD=root;'
            'TrustServerCertificate=yes'
        )
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return None

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.df: Optional[pd.DataFrame] = None
        self.archivo_excel: Optional[str] = None
        self.campos_a_actualizar = []

        self.title("Helados Cali - Gestor de Precios")
        self.geometry("1280x800")
        self.configure(bg=COLORES["fondo"])
        
        # Configurar el estilo de la tabla
        configurar_estilo_tabla()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_panel_lateral()
        self.crear_marco_principal()

    def crear_panel_lateral(self):
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color=COLORES["primario"],
            width=250,
            corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Logo y título
        try:
            img_path = os.path.join(os.path.dirname(__file__), "cali.png")
            image = Image.open(img_path).resize((180, 80))
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_label = ctk.CTkLabel(
                self.sidebar_frame,
                image=self.logo_image,
                text=""
            )
            self.logo_label.grid(row=0, column=0, pady=(40, 20))
        except Exception as e:
            print(f"No se pudo cargar la imagen del logo: {e}")

        # Título de la aplicación
        titulo = ctk.CTkLabel(
            self.sidebar_frame,
            text="Gestor de Precios",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORES["texto_claro"]
        )
        titulo.grid(row=1, column=0, pady=(0, 30))

        # Botones
        self.btn_cargar_excel = ctk.CTkButton(
            self.sidebar_frame,
            text="Cargar Excel",
            font=ctk.CTkFont(size=15),
            fg_color=COLORES["acento"],
            text_color=COLORES["texto_claro"],
            hover_color=COLORES["hover"],
            height=40,
            corner_radius=8,
            command=self.cargar_excel
        )
        self.btn_cargar_excel.grid(row=2, column=0, padx=20, pady=10)

        self.btn_actualizar = ctk.CTkButton(
            self.sidebar_frame,
            text="Actualizar BD",
            font=ctk.CTkFont(size=15),
            fg_color=COLORES["acento"],
            text_color=COLORES["texto_claro"],
            hover_color=COLORES["hover"],
            height=40,
            corner_radius=8,
            command=self.actualizar_datos_en_bd
        )
        self.btn_actualizar.grid(row=3, column=0, padx=20, pady=10)

        # Versión en la parte inferior
        version = ctk.CTkLabel(
            self.sidebar_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=12),
            text_color=COLORES["acento_claro"]
        )
        version.grid(row=5, column=0, pady=(0, 20))

    def crear_marco_principal(self):
        # Marco principal con efecto de elevación
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=COLORES["fondo_tabla"],
            corner_radius=15,
            border_width=1,
            border_color=COLORES["borde"]
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        # Título con estilo moderno
        titulo_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        titulo_frame.pack(fill="x", padx=20, pady=(20, 0))

        gradient_label = ctk.CTkLabel(
            titulo_frame,
            text="Sistema de Gestión de Precios",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORES["texto_oscuro"]
        )
        gradient_label.pack(side="left", pady=(0, 10))

        # Área de contenido inicial
        self.contenido_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.contenido_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Mensaje inicial
        mensaje_inicial = ctk.CTkLabel(
            self.contenido_frame,
            text="Carga un archivo Excel para comenzar",
            font=ctk.CTkFont(size=16),
            text_color=COLORES["acento"]
        )
        mensaje_inicial.pack(expand=True)

    def cargar_excel(self):
        filename = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
        if filename:
            try:
                self.archivo_excel = filename
                self.df = pd.read_excel(filename)
                if 'codprod' not in self.df.columns:
                    self.mostrar_mensaje("El archivo debe contener la columna 'codprod'")
                    self.df = None
                    return
                self.campos_a_actualizar = []
                self.mostrar_tabla_excel()
            except Exception as e:
                self.mostrar_mensaje(f"Error al cargar el archivo: {str(e)}")

    def mostrar_tabla_excel(self):
        # Limpiar main_frame manteniendo el título
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

        # Frame para selección de columnas con estilo moderno
        selector_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color=COLORES["fondo"],
            corner_radius=8
        )
        selector_frame.pack(fill="x", padx=5, pady=(0, 15))

        # Frame interno para los checkboxes
        checks_frame = ctk.CTkFrame(
            selector_frame,
            fg_color="transparent"
        )
        checks_frame.pack(fill="x", padx=10, pady=10)

        self.col_vars = {}
        columnas = [col for col in self.df.columns if col != 'codprod']

        def toggle_col(col):
            if self.col_vars[col].get():
                if col not in self.campos_a_actualizar:
                    self.campos_a_actualizar.append(col)
            else:
                if col in self.campos_a_actualizar:
                    self.campos_a_actualizar.remove(col)

        # Botón seleccionar todas con estilo mejorado
        self.select_all_var = tk.BooleanVar(value=False)
        def toggle_all():
            val = self.select_all_var.get()
            for col in columnas:
                self.col_vars[col].set(val)
                if val and col not in self.campos_a_actualizar:
                    self.campos_a_actualizar.append(col)
                elif not val and col in self.campos_a_actualizar:
                    self.campos_a_actualizar.remove(col)

        btn_all = ctk.CTkCheckBox(
            checks_frame,
            text="Seleccionar todas",
            variable=self.select_all_var,
            command=toggle_all,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLORES["acento"],
            hover_color=COLORES["hover"],
            text_color=COLORES["texto_oscuro"]
        )
        btn_all.pack(side="left", padx=8)

        # Checkboxes de columnas con estilo mejorado
        for col in columnas:
            self.col_vars[col] = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                checks_frame,
                text=col,
                variable=self.col_vars[col],
                command=lambda c=col: toggle_col(c),
                font=ctk.CTkFont(size=13),
                fg_color=COLORES["acento"],
                hover_color=COLORES["hover"],
                text_color=COLORES["texto_oscuro"]
            )
            cb.pack(side="left", padx=4)

        # Frame para la tabla con scroll
        table_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color=COLORES["fondo_tabla"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear frame con scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        # Tabla mejorada
        tree = ttk.Treeview(
            table_frame,
            columns=list(self.df.columns),
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        # Configurar scrollbars
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        # Configurar columnas
        for col in self.df.columns:
            tree.heading(col, text=col)
            # Ajustar ancho según el contenido
            max_width = max(
                len(str(self.df[col].max())),
                len(str(self.df[col].min())),
                len(col)
            ) * 10
            tree.column(col, width=min(max_width, 200), anchor="center")

        # Insertar datos con estilo alternado
        for i, (_, row) in enumerate(self.df.head(100).iterrows()):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.insert("", "end", values=list(row), tags=(tag,))

        # Configurar colores alternados para las filas
        tree.tag_configure('odd', background=COLORES["fondo"])
        tree.tag_configure('even', background=COLORES["fondo_tabla"])

        tree.pack(fill="both", expand=True)

        # Mensaje de ayuda con estilo mejorado
        ayuda_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color="transparent"
        )
        ayuda_frame.pack(fill="x", pady=(10, 0))

        ayuda = ctk.CTkLabel(
            ayuda_frame,
            text="Selecciona las columnas a actualizar. La columna 'codprod' es obligatoria y no editable.",
            font=ctk.CTkFont(size=13),
            text_color=COLORES["acento"]
        )
        ayuda.pack(pady=5)

        # Información del archivo
        info_archivo = ctk.CTkLabel(
            ayuda_frame,
            text=f"Archivo: {os.path.basename(self.archivo_excel)} • Registros: {len(self.df)}",
            font=ctk.CTkFont(size=12),
            text_color=COLORES["secundario"]
        )
        info_archivo.pack(pady=(0, 5))

    def mostrar_mensaje(self, mensaje: str):
        # Limpiar contenido_frame
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

        # Crear frame para el mensaje
        mensaje_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color=COLORES["fondo"],
            corner_radius=8
        )
        mensaje_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Mostrar el mensaje con estilo
        texto = ctk.CTkTextbox(
            mensaje_frame,
            font=ctk.CTkFont(size=13),
            text_color=COLORES["texto_oscuro"],
            fg_color="transparent",
            corner_radius=0,
            wrap="word",
            height=200
        )
        texto.pack(fill="both", expand=True, padx=15, pady=15)
        texto.insert("1.0", mensaje)
        texto.configure(state="disabled")

    def actualizar_datos_en_bd(self):
        if self.df is None or not self.campos_a_actualizar:
            self.mostrar_mensaje("No hay datos cargados o campos seleccionados.")
            return

        conn = obtener_conexion()
        if conn is None:
            self.mostrar_mensaje("Error al conectar con la base de datos.")
            return

        cursor = conn.cursor()
        errores = 0
        actualizados = 0

        for _, fila in self.df.iterrows():
            codprod = fila.get("codprod")
            if pd.isna(codprod):
                errores += 1
                continue

            campos_set = []
            valores = []

            for campo in self.campos_a_actualizar:
                valor = fila.get(campo)
                if pd.isna(valor):
                    valor = None
                campos_set.append(f"{campo} = ?")
                valores.append(valor)

            valores.append(codprod)

            try:
                sql = f"UPDATE SAPROD SET {', '.join(campos_set)} WHERE CODPROD = ?"
                cursor.execute(sql, valores)
                actualizados += 1
            except Exception as e:
                errores += 1
                print(f"Error en fila con codprod {codprod}: {e}")

        conn.commit()
        conn.close()

        self.mostrar_mensaje(f"Actualización completada.\nRegistros actualizados: {actualizados}\nErrores: {errores}")

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()