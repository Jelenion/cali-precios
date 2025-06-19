import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import pandas as pd
from typing import Optional
import os
from DB.connection import update_producto

# Configuración de colores corporativos
COLORES = {
    "primario": "#003B73",
    "secundario": "#D61A1F",
    "acento": "#FFFFFF",
    "texto_claro": "#FFFFFF",
    "texto_oscuro": "#000000",
    "fondo_tabla": "#e6f0fa",
    "fondo_encabezado": "#003B73",
    "texto_encabezado": "#FFFFFF"
}

# Campos que se pueden actualizar
CAMPOS_COSTOS = ["costact", "costprom", "costant"]
CAMPOS_PRECIOS = ["precio1", "precio2", "precio3"]
ARCHIVO_EXCEL = "datos.xlsx"

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.df: Optional[pd.DataFrame] = None
        self.campos_actualizables = []
        self.title("Helados Cali - Sistema de Gestión")
        self.geometry("1200x750")
        self.state('zoomed')  # Abrir siempre maximizada
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.crear_panel_lateral()
        self.crear_marco_principal()
        self.estilizar_treeview()
        self.cargar_excel_automatico()

    def crear_panel_lateral(self):
        self.sidebar_frame = ctk.CTkFrame(
            self, fg_color=COLORES["primario"], width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Menú Principal",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORES["texto_claro"])
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        self.btn_actualizar = ctk.CTkButton(
            self.sidebar_frame, text="Actualizar Base de Datos",
            fg_color=COLORES["secundario"], text_color=COLORES["texto_claro"],
            hover_color="#AA1518", command=self.actualizar_base_datos)
        self.btn_actualizar.grid(row=1, column=0, padx=20, pady=10)

    def crear_marco_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORES["fondo_tabla"])
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_label = ctk.CTkLabel(
            self.main_frame, text="Sistema de Gestión de Productos",
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORES["primario"])
        self.main_label.pack(pady=10)
        # Botón de recarga visual (emoji)
        self.btn_reload = tk.Button(
            self.main_frame, text="🔄", font=("Arial", 18, "bold"),
            command=self.recargar_excel, bd=0, bg=COLORES["fondo_tabla"],
            activebackground=COLORES["fondo_tabla"]
        )
        self.btn_reload.place(relx=0.97, rely=0.01, anchor="ne")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=COLORES["fondo_tabla"],
                        fieldbackground=COLORES["fondo_tabla"],
                        font=("Arial", 14),
                        rowheight=32)
        style.configure("Treeview.Heading",
                        background=COLORES["fondo_encabezado"],
                        foreground=COLORES["texto_encabezado"],
                        font=("Arial", 15, "bold"))
        self.tree = ttk.Treeview(self.main_frame, show="headings")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.bind('<Double-1>', self.editar_celda)

    def estilizar_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=COLORES["fondo_tabla"],
                        fieldbackground=COLORES["fondo_tabla"],
                        font=("Arial", 14),
                        rowheight=32)
        style.configure("Treeview.Heading",
                        background=COLORES["fondo_encabezado"],
                        foreground=COLORES["texto_encabezado"],
                        font=("Arial", 15, "bold"))

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
        # Efecto de parpadeo profesional: ocultar la tabla, esperar, recargar datos y mostrarla con tamaño correcto
        self.tree.pack_forget()
        self.update_idletasks()
        def mostrar_y_reaplicar():
            self.leer_y_mostrar_excel()
            self.tree.pack(pady=10, padx=10, fill="both", expand=True)
            columnas_a_mostrar = ['codprod'] + self.campos_actualizables
            for col in columnas_a_mostrar:
                self.tree.column(col, width=160, anchor="center")
        self.after(200, mostrar_y_reaplicar)

    def mostrar_datos_en_tabla(self, df):
        self.tree.delete(*self.tree.get_children())
        # Eliminar todas las columnas previas
        for col in self.tree['columns']:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        columnas_a_mostrar = ['codprod'] + self.campos_actualizables
        self.tree['columns'] = columnas_a_mostrar
        for col in columnas_a_mostrar:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=260, anchor="center", stretch=False)
        for idx, row in df.iterrows():
            values = [row.get(col, '') for col in columnas_a_mostrar]
            self.tree.insert('', 'end', iid=idx, values=values)
        # Forzar el tamaño fijo después de insertar
        self.tree.update_idletasks()
        for col in columnas_a_mostrar:
            self.tree.column(col, width=260, anchor="center", stretch=False)

    def editar_celda(self, event):
        """Permite editar una celda de la tabla (excepto codprod)."""
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
        entry = tk.Entry(self.tree, font=("Arial", 14))
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, valor_actual)
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
        resultados = []
        for idx, row in self.df.iterrows():
            codprod = row['codprod']
            campos_dict = {campo: row[campo] for campo in self.campos_actualizables if campo in row}
            exito, error = update_producto(codprod, campos_dict)
            if exito:
                resultados.append((codprod, "Actualizado", ""))
            else:
                resultados.append((codprod, "Error", error))
        # Guardar los cambios en el Excel
        try:
            self.df.to_excel(self.archivo_excel, index=False)
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo guardar el archivo Excel: {str(e)}")
        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        self.tree.delete(*self.tree.get_children())
        # Eliminar todas las columnas previas
        for col in self.tree['columns']:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        self.tree['columns'] = ["codprod", "estado", "detalle"]
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=1100, anchor="center", stretch=False)
        for codprod, estado, detalle in resultados:
            self.tree.insert('', 'end', values=(codprod, estado, detalle))
        # Forzar el tamaño fijo después de insertar
        self.tree.update_idletasks()
        for col in self.tree['columns']:
            self.tree.column(col, width=1100, anchor="center", stretch=False)
