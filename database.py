from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://@LEONARDO-PC\\SQLEXPRESS/personas"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Inicializar SQLAlchemy con la app Flask
    db.init_app(app)
