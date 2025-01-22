from flask import Flask
from database import init_db, db
from sqlalchemy.sql import text
from routes import register_routes

from flask_migrate import Migrate
from models import Persona  # importa modelo persona

# Crear la app Flask
app = Flask(__name__)

# Inicializar la base de datos
init_db(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Registrar rutas
register_routes(app)


@app.route("/")
def index():
    return "¡Servidor funcionando correctamente!!"


@app.route("/test_db")
def test_db():
    try:
        with db.engine.connect() as connection:
            # Ejecutar consulta usando text()
            result = connection.execute(text("SELECT 1 AS test_column"))
            # Acceder a los resultados usando índices numéricos
            result_list = [row[0] for row in result]

            return {"status": "Conexion exitosa", "result": result_list}

    except Exception as e:
        return {"status": "Error en la conexión", "error": str(e)}


if __name__ == "__main__":
    app.run(debug=True)
