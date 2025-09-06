from database.connection import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT GETDATE()"))
            fecha = result.scalar_one()  # Obtiene el valor de la primera columna
            print("✅ Conexión exitosa! Fecha en SQL Server:", fecha)
    except Exception as e:
        print("❌ Error en la conexión:", e)

if __name__ == "__main__":
    test_connection()
