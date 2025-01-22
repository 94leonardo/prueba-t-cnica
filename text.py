import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LEONARDO-PC\\SQLEXPRESS;"
    "DATABASE=personas;"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Conexión exitosa a SQL Server")
    conn.close()
except Exception as e:
    print(f"Error al conectar a SQL Server: {e}")
