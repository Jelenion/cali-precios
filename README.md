# Sistema de Gestión de Precios Cali (Cali-Precios)

Sistema de gestión y actualización de precios para Helados Cali, diseñado para procesar y mantener actualizada la información de productos y precios mediante archivos Excel.

## 🎯 Características Principales

- Interfaz gráfica moderna con colores corporativos de Helados Cali
- Procesamiento de archivos Excel para gestión de productos
- Validación automática de datos y columnas requeridas
- Visualización y edición directa de información de productos
- Sistema de actualización de precios y costos en base de datos y Excel
- Botón de recarga visual con efecto profesional
- Icono personalizado en ventana y barra de tareas (al compilar)

## 📋 Requisitos del Sistema

### Software Necesario
- Python 3.x
- tkinter
- customtkinter
- pandas (para manejo de archivos Excel)
- openpyxl (para soporte de archivos Excel)

### Requisitos del Archivo Excel
El archivo Excel debe contener las siguientes columnas:
- `codprod` (Código de Producto) - **Obligatorio**
- `costAct`, `costprom`, `costant` (Costos) - Opcionales
- `precio1`, `precio2`, `precio3` (Precios) - Opcionales

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/[tu-usuario]/cali-precios.git
cd cali-precios
```

2. Crear un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso en modo desarrollo

Para iniciar la aplicación:
```bash
python main.py
```

## 🖼️ Icono personalizado en la barra de tareas (Windows)

Para que el icono personalizado se muestre en la barra de tareas de Windows, debes compilar el programa con PyInstaller:

1. Instala PyInstaller:
```bash
pip install pyinstaller
```

2. Asegúrate de tener un archivo de icono llamado `cali_precios.ico` en la raíz del proyecto. Puedes crear uno en [favicon.io](https://favicon.io/) o [icons8.com](https://icons8.com/icons/set/ice-cream).

3. Compila el programa:
```bash
pyinstaller --onefile --windowed --icon=cali_precios.ico main.py
```

4. Ejecuta el archivo `.exe` generado en la carpeta `dist/` y verás el icono personalizado en la ventana y la barra de tareas.

## 🧊 Cómo crear un icono .ico profesional

- Puedes usar [favicon.io](https://favicon.io/) para convertir una imagen PNG a .ico.
- O descargar un icono de [icons8.com](https://icons8.com/icons/set/ice-cream) o [flaticon.com](https://www.flaticon.com/).
- El icono debe ser cuadrado (por ejemplo, 256x256 px) y guardarse como `cali_precios.ico` en la raíz del proyecto.

## 🎨 Diseño

La aplicación utiliza los colores corporativos de Helados Cali:
- Azul Corporativo: `#003B73`
- Rojo Corporativo: `#D61A1F`

## 👥 Contribución

Si deseas contribuir al proyecto:
1. Haz un Fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ✨ Agradecimientos

- Equipo de Helados Cali
- Contribuidores y desarrolladores
