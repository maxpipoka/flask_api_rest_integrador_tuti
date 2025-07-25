from flask import Blueprint, request, jsonify

from src.utils.decorators import token_required, require_json, handle_api_exceptions

from ..models.schemas import TutorSchema

from bussiness_logic.tutor_logic import TutorLogic

bp = Blueprint("tutores", __name__)

# Definición de atajos de serializador
tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)


# Definicion endpoint obtiene todos los tutores activos
@bp.route("/tutores", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error al obtener los tutores activos")
def get_tutors():
    """
    Endpoint to get all active tutors.
    Returns:
        JSON: A list of active tutors.
    Raises:
        ValueError: If no active tutors are found.
        SQLAlchemyError: If there is an error querying the database.
        Exception: For any other exception that occurs.
    """

    tutor_logic = TutorLogic()

    all_active_tutors = tutor_logic.get_tutors()

    return jsonify(all_active_tutors), 200


# Definición endpoint obtiene un solo tutor filtrado por id
@bp.route("/tutores/<id>", methods=["GET"])
@token_required
def get_tutor_by_id(id):
    """
    Endpoint to get a tutor by their ID.
    Args:
        id (int): The ID of the tutor to retrieve.
    Returns:
        JSON: A dictionary representing the found tutor.
    Raises:
        ValueError: If no tutor is found with the provided ID.
        SQLAlchemyError: If there is an error querying the database.
        Exception: For any other exception that occurs.
    """

    tutor_logic = TutorLogic()

    founded_tutor = tutor_logic.get_tutor_by_id(id)

    return jsonify(founded_tutor.as_dict()), 200


# Definicion endpoint que borra un tutor, cambia el activo
@bp.route("/tutores/<id>", methods=["DELETE"])
@token_required
@handle_api_exceptions(default_message="Error al eliminar el tutor")
def delete_tutor(id):
    """
    Endpoint to delete a tutor by their ID.
    Args:
        id (int): The ID of the tutor to delete.
    Returns:
        JSON: A success or error message.
    Raises:
        ValueError: If no tutor is found with the provided ID.
        SQLAlchemyError: If there is an error querying the database.
        Exception: For any other exception that occurs.
    """

    tutor_logic = TutorLogic()

    tutor_to_delete = tutor_logic.delete_tutor(id)

    return jsonify(tutor_to_delete.as_dict()), 200


# Definicion endpoint creacion tutor
@bp.route("/tutores", methods=["POST"])
@token_required
@require_json
@handle_api_exceptions(default_message="Error al guardar el tutor")
def save_tutor():
    """
    Endpoint to create a new tutor.
    Returns:
        JSON: The created tutor.
    Raises:
        ValueError: If there is an error creating the tutor or if the data is invalid.
        SQLAlchemyError: If there is an error querying the database.
        Exception: For any other exception that occurs.
    """

    tutor_logic = TutorLogic()

    new_tutor = tutor_logic.save_tutor(tutor_data=request.json)

    return jsonify(new_tutor.as_dict()), 201


# Deficion endpoint edicion tutor
@bp.route("/tutores/<id>", methods=["PATCH"])
@token_required
@require_json
@handle_api_exceptions(default_message="Error al actualizar el tutor")
def update_tutor(id):
    """
    Endpoint to update a tutor by their ID.
    Args:
        id (int): The ID of the tutor to update.
    Returns:
        JSON: The updated tutor.
    Raises:
        ValueError: If no tutor is found with the provided ID or if there is no data to update.
        SQLAlchemyError: If there is an error querying the database.
        Exception: For any other exception that occurs.
    """

    if not id:
        return jsonify({"message": "ID del tutor es requerido"}), 400

    tutor_logic = TutorLogic()

    tutor_to_update = tutor_logic.update_tutor(id, tutor_data=request.json)

    return jsonify(tutor_to_update), 201
