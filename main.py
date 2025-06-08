# Importar la clase principal de la interfaz gráfica
from GUI.gui import AppGUI

def main():
    """Función principal que inicia la aplicación"""
    app = AppGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
