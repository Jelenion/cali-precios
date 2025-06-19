# Importar la clase principal de la interfaz gráfica
import os
import sys

# Forzar el icono en la barra de tareas ANTES de crear la ventana
icon_path = 'cali_precios.ico'
if sys.platform == "win32" and os.path.exists(icon_path):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'cali.precios.icon')

from GUI.gui import AppGUI

def main():
    """Función principal que inicia la aplicación"""
    app = AppGUI()
    if os.path.exists(icon_path):
        app.iconbitmap(icon_path)
    app.mainloop()

if __name__ == "__main__":
    main()
