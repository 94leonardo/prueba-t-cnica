from flask import Blueprint, jsonify, request
from models import Persona, db

# crear un blueprint para las rutas

api = Blueprint("api", __name__)

# 1 . obtener toda las personas


@api.route("/personas", methods=["GET"])
def obtener_personas():
    personas = Persona.query.all()
    return jsonify(
        [
            {
                "id": p.id,
                "nombre": p.nombre,
                "edad": p.edad,
                "tipo": p.tipo,
                "email": p.email,
            }
            for p in personas
        ]
    )


# 2 obtener una persona por ID


@api.route("/personas/<int:id>", methods=["GET"])
def obtener_persona(id):
    persona = Persona.query.get(id)

    try:
        if persona is None:
            return jsonify({"error": "Persona no encontrada"}), 404
        return jsonify(
            {
                "id": persona.id,
                "nombre": persona.nombre,
                "edad": persona.edad,
                "tipo": persona.tipo,
                "email": persona.email,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3. Crear una nueva persona


@api.route("/personas", methods=["POST"])
def crear_persona():
    data = request.get_json()

    try:
        # Verificar si el cuerpo es una lista
        if isinstance(data, list):
            nuevas_personas = []
            for persona_data in data:
                # Validar campos obligatorios
                if not all(
                    key in persona_data for key in ["nombre", "edad", "tipo", "email"]
                ):
                    return (
                        jsonify(
                            {
                                "error": "Todos los campos (nombre, edad, tipo, email) son obligatorios"
                            }
                        ),
                        400,
                    )

                nueva_persona = Persona(
                    nombre=persona_data["nombre"],
                    edad=persona_data["edad"],
                    tipo=persona_data["tipo"],
                    email=persona_data["email"],
                )
                nuevas_personas.append(nueva_persona)
                db.session.add(nueva_persona)

            # Confirmar los cambios en la base de datos
            db.session.commit()
            return (
                jsonify(
                    {
                        "mensaje": f"{len(nuevas_personas)
                                   } personas creadas exitosamente"
                    }
                ),
                201,
            )

        # Procesar un único registro
        else:
            # Validar campos obligatorios
            if not all(key in data for key in ["nombre", "edad", "tipo", "email"]):
                return (
                    jsonify(
                        {
                            "error": "Todos los campos (nombre, edad, tipo, email) son obligatorios"
                        }
                    ),
                    400,
                )

            nueva_persona = Persona(
                nombre=data["nombre"],
                edad=data["edad"],
                tipo=data["tipo"],
                email=data["email"],
            )
            db.session.add(nueva_persona)
            db.session.commit()
            return jsonify({"mensaje": "Persona creada exitosamente"}), 201

    except Exception as e:
        # Manejo de errores generales
        db.session.rollback()  # Revertir la transacción en caso de error
        return (
            jsonify(
                {"error": "Ocurrió un error durante la creación", "detalle": str(e)}
            ),
            500,
        )


# 4. Actualizar una persona por ID


@api.route("/personas/<int:id>", methods=["PUT"])
def actualizar_persona(id):
    persona = Persona.query.get(id)

    try:
        if persona is None:
            return jsonify({"error": "Persona no encontrada"}), 404

        data = request.get_json()
        persona.nombre = data["nombre"]
        persona.edad = data["edad"]
        persona.tipo = data["tipo"]
        persona.email = data["email"]

        db.session.commit()

        return jsonify({"mensaje": "Persona actualizada exitosamente"}), 202

    except Exception as e:
        db.session.rollback()  # Revertir la transacción en caso de error
        return (
            jsonify(
                {
                    "error": "Ocurrió un error durante la sctualizacion",
                    "detalle": str(e),
                }
            ),
            500,
        )


# 5. Eliminar una persona por ID


@api.route("/personas/<int:id>", methods=["DELETE"])
def eliminar_persona(id):
    persona = Persona.query.get(id)

    try:
        if persona is None:

            return jsonify({"error": "Persona no encontrada"}), 404

        db.session.delete(persona)
        db.session.commit()

        return jsonify({"mensaje": "Persona eliminada exitosamente"}),202

    except Exception as e:
        db.session.rollback()  # Revertir la transacción en caso de error
        return (
            jsonify(
                {
                    "error": "Ocurrió un error durante la Eliminación",
                    "detalle": str(e),
                }
            ),
            500,
        )
# Registrar las rutas en la aplicación


def register_routes(app):
    app.register_blueprint(api)
