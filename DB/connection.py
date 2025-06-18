# Conexion con SQL server
import pyodbc

# Parámetros de conexión
server = 'DESKTOP-ETTD339'  # Ejemplo: 'localhost\\SQLEXPRESS'
database = 'hcdb2'
username = 'sa'
password = '12345678'

try:
    # Establecer conexión
    conexion = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    
    print("Conexión exitosa a SQL Server")

    # # Crear cursor para ejecutar comandos SQL
    # cursor = conexion.cursor()

    # # Ejemplo: leer datos
    # cursor.execute("SELECT * FROM TuTabla")
    # filas = cursor.fetchall()

    # for fila in filas:
    #     print(fila)

except Exception as e:
    print("Error al conectar con SQL Server:", e)

# finally:
#     # Cerrar conexión
#     if 'conexion' in locals():
#         conexion.close()
#         print("Conexión cerrada")

