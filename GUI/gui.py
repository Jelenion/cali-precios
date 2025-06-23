import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import pandas as pd
import pyodbc
from typing import Optional
from PIL import Image, ImageTk
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

COLORES = {
    "primario": "#001F54",
    "secundario": "#FF6B6B",
    "acento": "#4ECDC4",
    "fondo": "#F0F4F8",
    "texto_claro": "#FFFFFF",
    "texto_oscuro": "#1A1A1A"
}

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
        self.geometry("1200x700")
        self.configure(bg=COLORES["fondo"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_panel_lateral()
        self.crear_marco_principal()

    def crear_panel_lateral(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=COLORES["primario"], width=230, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        try:
            img_path = os.path.join(os.path.dirname(__file__), "cali.png")
            image = Image.open(img_path).resize((180, 80))
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
            self.logo_label.grid(row=0, column=0, pady=(30, 10))
        except Exception as e:
            print(f"No se pudo cargar la imagen del logo: {e}")

        self.btn_cargar_excel = ctk.CTkButton(
            self.sidebar_frame, text="Cargar Excel", font=ctk.CTkFont(size=15),
            fg_color=COLORES["secundario"], text_color=COLORES["texto_claro"],
            hover_color="#FF4C4C", command=self.cargar_excel
        )
        self.btn_cargar_excel.grid(row=1, column=0, padx=20, pady=10)

        self.btn_mostrar_datos = ctk.CTkButton(
            self.sidebar_frame, text="Mostrar Datos", font=ctk.CTkFont(size=15),
            fg_color=COLORES["secundario"], text_color=COLORES["texto_claro"],
            hover_color="#FF4C4C", command=self.mostrar_datos
        )
        self.btn_mostrar_datos.grid(row=2, column=0, padx=20, pady=10)

        self.btn_actualizar = ctk.CTkButton(
            self.sidebar_frame, text="Actualizar BD", font=ctk.CTkFont(size=15),
            fg_color=COLORES["secundario"], text_color=COLORES["texto_claro"],
            hover_color="#FF4C4C", command=self.actualizar_datos_en_bd
        )
        self.btn_actualizar.grid(row=3, column=0, padx=20, pady=10)

    def crear_marco_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        gradient_label = ctk.CTkLabel(
            self.main_frame, text="Sistema de Gestión de Precios", height=60,
            font=ctk.CTkFont(size=28, weight="bold"), text_color=COLORES["primario"]
        )
        gradient_label.pack(pady=(20, 10))

        self.text_area = ctk.CTkTextbox(
            self.main_frame, width=800, height=500,
            font=ctk.CTkFont(size=13), text_color=COLORES["texto_oscuro"],
            fg_color="#FAFAFA", corner_radius=12, wrap="word"
        )
        self.text_area.pack(pady=10, padx=15, fill="both", expand=True)

    def cargar_excel(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Selecciona campos a actualizar")
        ventana.geometry("380x430")
        ventana.configure(bg="#ffffff")

        opciones = ["costAct", "costAnt", "costPro", "precioi1", "precioi2", "precioi3"]

        label = ctk.CTkLabel(ventana, text="Selecciona los campos a actualizar:", font=ctk.CTkFont(size=16, weight="bold"))
        label.pack(pady=15)

        self.check_vars = {}

        for campo in opciones:
            var = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(ventana, text=campo, variable=var, font=ctk.CTkFont(size=14))
            cb.pack(anchor="w", padx=30, pady=6)
            self.check_vars[campo] = var

        btn_confirmar = ctk.CTkButton(
            ventana, text="Confirmar y cargar Excel", font=ctk.CTkFont(size=14),
            fg_color=COLORES["acento"], text_color=COLORES["texto_oscuro"],
            command=lambda v=ventana: self.confirmar_campos_y_cargar(v)
        )
        btn_confirmar.pack(pady=25)

    def confirmar_campos_y_cargar(self, ventana_popup):
        campos_seleccionados = [campo for campo, var in self.check_vars.items() if var.get()]
        if not campos_seleccionados:
            self.mostrar_mensaje("Debes seleccionar al menos un campo para actualizar.")
            return

        ventana_popup.destroy()

        try:
            filename = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
            if filename:
                self.archivo_excel = filename
                self.df = pd.read_excel(filename)

                if 'codprod' not in self.df.columns:
                    self.mostrar_mensaje("El archivo debe contener la columna 'codprod'")
                    self.df = None
                    return

                mensaje = f"Archivo cargado: {filename}\n"
                mensaje += f"Campos seleccionados: {', '.join(campos_seleccionados)}\n"
                mensaje += f"Columnas encontradas: {', '.join(self.df.columns)}\n"

                faltantes = [campo for campo in campos_seleccionados if campo not in self.df.columns]
                if faltantes:
                    mensaje += f"\nCampos faltantes: {', '.join(faltantes)}"

                self.mostrar_mensaje(mensaje)
                self.campos_a_actualizar = campos_seleccionados
        except Exception as e:
            self.mostrar_mensaje(f"Error al cargar el archivo: {str(e)}")

    def mostrar_datos(self):
        if self.df is not None:
            info = f"Resumen del archivo:\n"
            info += f"Total de registros: {len(self.df)}\n"
            info += f"Columnas disponibles: {', '.join(self.df.columns)}\n\n"
            info += "Primeros 10 registros:\n"
            info += str(self.df.head(10))
            self.mostrar_mensaje(info)
        else:
            self.mostrar_mensaje("No hay datos cargados. Por favor, cargue un archivo Excel primero.")

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

    def mostrar_mensaje(self, mensaje: str):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", mensaje)

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()