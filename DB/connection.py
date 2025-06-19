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

def update_producto(codprod, campos_dict):
    """
    Actualiza los campos indicados para el producto con el codprod dado.
    campos_dict: diccionario {campo: valor}
    """
    if not campos_dict:
        return False, "No hay campos para actualizar"
    try:
        cursor = conexion.cursor()
        set_clauses = []
        valores = []
        for campo, valor in campos_dict.items():
            set_clauses.append(f"{campo} = ?")
            valores.append(valor)
        sql = f"UPDATE SAPROD SET {', '.join(set_clauses)} WHERE codprod = ?"
        valores.append(codprod)
        cursor.execute(sql, valores)
        conexion.commit()
        return True, None
    except Exception as e:
        return False, str(e)

