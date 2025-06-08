# Sistema de Gestión de Precios Cali (Cali-Precios)

Sistema de gestión y actualización de precios para Helados Cali, diseñado para procesar y mantener actualizada la información de productos y precios mediante archivos Excel.

## 🎯 Características Principales

- Interfaz gráfica moderna con colores corporativos de Helados Cali
- Procesamiento de archivos Excel para gestión de productos
- Validación automática de datos y columnas requeridas
- Visualización de información de productos
- Sistema de actualización de precios y costos

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
- `costAct` (Costo Actual) - Recomendado
- `precio` (Precio) - Recomendado

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

## 💻 Uso

Para iniciar la aplicación:
```bash
python main.py
```

### Pasos para usar la aplicación:
1. Click en "Cargar Excel" para seleccionar el archivo de productos
2. El sistema validará automáticamente las columnas requeridas
3. Use "Mostrar Datos" para visualizar la información cargada

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