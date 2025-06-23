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

COLUMN_ALIASES = {
    "costAct": "Costo Actual",
    "costAnt": "Costo Anterior",
    "costPro": "Costo Promedio",
    "precioi1": "Precio 1",
    "precioi2": "Precio 2",
    "precioi3": "Precio 3",
    "codprod": "Código Producto"
}

def configurar_estilo_tabla():
    style = ttk.Style()
    style.theme_use('default')
    
    # Fuente moderna para filas y encabezados
    fuente_fila = ('Segoe UI', 12)
    fuente_encabezado = ('Segoe UI Semibold', 13)

    # Configurar el estilo de la tabla
    style.configure(
        "Custom.Treeview",
        background=COLORES["fondo_tabla"],
        foreground=COLORES["texto_oscuro"],
        fieldbackground=COLORES["fondo_tabla"],
        borderwidth=0,
        rowheight=32,
        font=fuente_fila
    )
    
    # Configurar el estilo de los encabezados
    style.configure(
        "Custom.Treeview.Heading",
        background=COLORES["secundario"],
        foreground=COLORES["texto_claro"],
        borderwidth=1,
        relief="flat",
        font=fuente_encabezado
    )
    
    # Configurar selección
    style.map(
        "Custom.Treeview",
        background=[('selected', COLORES["acento"])],
        foreground=[('selected', COLORES["texto_claro"])]
    )

def obtener_conexion():
    import pyodbc
    # Detectar el driver instalado
    drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
    if not drivers:
        import tkinter.messagebox as mbox
        mbox.showerror("Error de conexión", "No se encontró ningún driver ODBC para SQL Server instalado.\nInstala 'ODBC Driver 18 for SQL Server' o 'ODBC Driver 17 for SQL Server'.")
        return None
    # Preferir el 18, luego el 17, luego el primero disponible
    driver = None
    for preferido in ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]:
        if preferido in drivers:
            driver = preferido
            break
    if not driver:
        driver = drivers[-1]
    try:
        conexion = pyodbc.connect(
            f'DRIVER={{{driver}}};'
            'SERVER=DESKTOP-ETTD339;'
            'DATABASE=hcdb2;'
            'UID=sa;'
            'PWD=12345678;'
            'TrustServerCertificate=yes'
        )
        return conexion
    except Exception as e:
        import tkinter.messagebox as mbox
        mbox.showerror("Error de conexión", f"Driver usado: {driver}\n{str(e)}")
        print("Error de conexión:", e)
        return None

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.df: Optional[pd.DataFrame] = None
        self.archivo_excel: Optional[str] = None
        self.campos_a_actualizar = []

        self.title("Helados Cali - Gestor de Precios")
        self.configure(bg=COLORES["fondo"])
        # Maximizar ventana de forma robusta multiplataforma
        self.after(100, self.maximizar_ventana)
        
        # Configurar el estilo de la tabla
        configurar_estilo_tabla()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_panel_lateral()
        self.crear_marco_principal()

    def maximizar_ventana(self):
        try:
            self.state('zoomed')  # Windows
        except Exception:
            try:
                self.attributes('-zoomed', True)  # Linux
            except Exception:
                # Fallback: pantalla completa
                self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

    def crear_panel_lateral(self):
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color=(COLORES["primario"], "#1a1a2e80"),  # Transparencia
            width=250,
            corner_radius=20,
            border_width=2,
            border_color=COLORES["borde"]
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
        # Marco principal con efecto de elevación y transparencia
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=(COLORES["fondo_tabla"], "#ffffffcc"),  # Transparencia
            corner_radius=25,
            border_width=2,
            border_color=COLORES["borde"]
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=35, pady=35)

        # Título con estilo moderno
        titulo_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        titulo_frame.pack(fill="x", padx=30, pady=(30, 0))

        gradient_label = ctk.CTkLabel(
            titulo_frame,
            text="Sistema de Gestión de Precios",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORES["texto_oscuro"]
        )
        gradient_label.pack(side="left", pady=(0, 10))

        # Área de contenido inicial
        self.contenido_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=(COLORES["fondo"], "#f5f5f7cc"),  # Transparencia
            corner_radius=18
        )
        self.contenido_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Mensaje inicial
        mensaje_inicial = ctk.CTkLabel(
            self.contenido_frame,
            text="Carga un archivo Excel para comenzar",
            font=ctk.CTkFont(size=18, weight="bold"),
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

        # Checkboxes de columnas con alias
        for col in columnas:
            self.col_vars[col] = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                checks_frame,
                text=COLUMN_ALIASES.get(col, col),
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

        # Tabla mejorada con alias en los encabezados
        display_columns = [col for col in self.df.columns]
        display_column_names = [COLUMN_ALIASES.get(col, col) for col in display_columns]
        tree = ttk.Treeview(
            table_frame,
            columns=display_column_names,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        # Configurar scrollbars
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        # Configurar columnas con alias
        for idx, col in enumerate(display_columns):
            alias = COLUMN_ALIASES.get(col, col)
            tree.heading(alias, text=alias)
            max_width = max(
                len(str(self.df[col].max())),
                len(str(self.df[col].min())),
                len(alias)
            ) * 10
            tree.column(alias, width=min(max_width, 200), anchor="center")

        # Insertar datos con fondo blanco en todas las filas
        for i, (_, row) in enumerate(self.df.head(100).iterrows()):
            values = [row[col] for col in display_columns]
            tree.insert("", "end", values=values)

        tree.pack(fill="both", expand=True)

        # Mensaje de ayuda con estilo mejorado
        ayuda_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color="transparent"
        )
        ayuda_frame.pack(fill="x", pady=(10, 0))

        ayuda = ctk.CTkLabel(
            ayuda_frame,
            text="Selecciona las columnas a actualizar. La columna 'Código Producto' es obligatoria y no editable.",
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

        # Validar valores vacíos o inválidos antes de actualizar
        codigos_vacios = []
        columnas_invalidas = set()
        for idx, fila in self.df.iterrows():
            codprod = fila.get("codprod")
            if pd.isna(codprod):
                codigos_vacios.append(f"Fila {idx+2} (Código vacío)")
                continue
            for campo in self.campos_a_actualizar:
                valor = fila.get(campo)
                if pd.isna(valor) or valor == "":
                    codigos_vacios.append(f"{COLUMN_ALIASES.get(campo, campo)} en Código {codprod}")

        if codigos_vacios or columnas_invalidas:
            mensaje = "No se realizó la actualización por los siguientes errores:\n\n"
            if codigos_vacios:
                mensaje += "Valores vacíos en: " + ", ".join(codigos_vacios[:10])
                if len(codigos_vacios) > 10:
                    mensaje += f" ... (total {len(codigos_vacios)})"
                mensaje += "\n"
            if columnas_invalidas:
                mensaje += "Valores inválidos en: " + ", ".join(list(columnas_invalidas)[:10])
                if len(columnas_invalidas) > 10:
                    mensaje += f" ... (total {len(columnas_invalidas)})"
                mensaje += "\n"
            self.mostrar_mensaje(mensaje)
            return

        conn = obtener_conexion()
        if conn is None:
            self.mostrar_mensaje("Error al conectar con la base de datos.")
            return

        cursor = conn.cursor()
        errores = 0
        actualizados = 0
        codigos_actualizados = []
        codigos_error = []

        for _, fila in self.df.iterrows():
            codprod = fila.get("codprod")
            if pd.isna(codprod):
                errores += 1
                codigos_error.append("(vacío)")
                continue

            # No actualizar si el costo es 0 (costAct, costAnt, costPro)
            costo_cero = False
            for cost_col in ["costAct", "costAnt", "costPro"]:
                if cost_col in self.df.columns:
                    valor = fila.get(cost_col)
                    if not pd.isna(valor) and float(valor) == 0:
                        costo_cero = True
                        break
            if costo_cero:
                errores += 1
                codigos_error.append(f"{codprod} (Costo en 0)")
                continue

            try:
                # Si se va a actualizar costAct, primero pasar el valor actual a costAnt y calcular costPro
                if "costAct" in self.campos_a_actualizar:
                    cursor.execute("SELECT costAct FROM SAPROD WHERE CODPROD = ?", codprod)
                    row = cursor.fetchone()
                    if row is not None:
                        valor_actual_costAct = row[0]
                        cursor.execute("UPDATE SAPROD SET costAnt = ? WHERE CODPROD = ? AND Activo = 1 AND EsEnser = 0", valor_actual_costAct, codprod)
                        # Calcular el nuevo costPro como promedio entre el nuevo costAct y el nuevo costAnt
                        nuevo_costAct = fila.get("costAct")
                        try:
                            costAnt_val = float(valor_actual_costAct) if valor_actual_costAct is not None else 0
                            costAct_val = float(nuevo_costAct) if nuevo_costAct is not None else 0
                            costPro = (costAnt_val + costAct_val) / 2
                        except Exception:
                            costPro = None
                        cursor.execute("UPDATE SAPROD SET costPro = ? WHERE CODPROD = ? AND Activo = 1 AND EsEnser = 0", costPro, codprod)
                # Ahora armar el update normal
                campos_set = []
                valores = []
                for campo in self.campos_a_actualizar:
                    valor = fila.get(campo)
                    if pd.isna(valor):
                        valor = None
                    campos_set.append(f"{campo} = ?")
                    valores.append(valor)
                valores.append(codprod)
                sql = f"UPDATE SAPROD SET {', '.join(campos_set)} WHERE CODPROD = ? AND Activo = 1 AND EsEnser = 0"
                result = cursor.execute(sql, valores)
                if cursor.rowcount > 0:
                    actualizados += 1
                    codigos_actualizados.append(str(codprod))
                else:
                    # Consultar motivo exacto
                    cursor.execute("SELECT Activo, EsEnser FROM SAPROD WHERE CODPROD = ?", codprod)
                    row = cursor.fetchone()
                    if row is not None:
                        activo_db, es_enser_db = row
                        if activo_db != 1:
                            codigos_error.append(f"{codprod} (No activo)")
                        elif es_enser_db != 0:
                            codigos_error.append(f"{codprod} (EsEnser ≠ 0)")
                        else:
                            codigos_error.append(f"{codprod} (No actualizado)")
                    else:
                        codigos_error.append(f"{codprod} (No encontrado en BD)")
                    errores += 1
            except Exception as e:
                errores += 1
                codigos_error.append(f"{codprod} (Error SQL)")
                self.mostrar_mensaje(f"Error en fila con Código Producto {codprod}: {e}")

        conn.commit()
        conn.close()

        resumen = f"Actualización completada.\n"
        resumen += f"Registros actualizados: {actualizados}\n"
        resumen += f"Errores: {errores}\n"
        resumen += f"Columnas actualizadas: {', '.join([COLUMN_ALIASES.get(c, c) for c in self.campos_a_actualizar])}\n\n"
        if codigos_actualizados:
            resumen += f"Códigos actualizados: {', '.join(codigos_actualizados[:20])}"
            if len(codigos_actualizados) > 20:
                resumen += f" ... (total {len(codigos_actualizados)})\n"
            else:
                resumen += "\n"
        if codigos_error:
            resumen += f"Códigos con error: {', '.join(codigos_error[:10])}"
            if len(codigos_error) > 10:
                resumen += f" ... (total {len(codigos_error)})\n"
            else:
                resumen += "\n"
        self.mostrar_mensaje(resumen)

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()