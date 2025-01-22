from database import db


class Persona(db.Model):

    __tablename__ = 'persona'  # nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # paciente o medico
    email = db.Column(db.String(100), nullable=False, unique=True)
