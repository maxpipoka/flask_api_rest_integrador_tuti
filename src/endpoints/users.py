from flask import Blueprint, jsonify, request

from bussiness_logic.user_logic import UserLogic
from src.utils.decorators import handle_api_exceptions, require_json, token_required

bp = Blueprint("usuarios", __name__)


@bp.route("/usuarios", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error al obtener los usuarios")
def get_users():
    """
    Gets all active users.
    Returns:
        Response: A JSON with a list of active users.
    Raises:
        ValueError: If no active users are found.
        Exception: If an error occurs while querying the database.
        404: If users cannot be retrieved.
    """

    user_logic = UserLogic()

    all_users = user_logic.get_users()

    return jsonify(all_users), 200


@bp.route("/usuarios/<id>", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error al obtener el usuario por ID")
def get_user_by_id(id):
    """
    Gets a user by their ID.
    Args:
        id (int): The ID of the user to retrieve.
    Returns:
        Response: A JSON with the found user's data.
    Raises:
        ValueError: If the user with the provided ID is not found.
        Exception: If an error occurs while querying the database.
        404: If the user is not found.
    """

    if not id:
        return jsonify({"message": "No se proporcionó el ID del usuario"}), 400

    user_logic = UserLogic()

    founded_user = user_logic.get_user_by_id(id)

    if not founded_user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(founded_user), 200


@bp.route("/usuarios", methods=["POST"])
@token_required
@require_json
@handle_api_exceptions(default_message="Error al registrar el usuario")
def save_user():
    """
    Saves a new user to the database.
    Returns:
        Response: A JSON with the saved user's data.
    Raises:
        ValueError: If required fields are missing in the user data.
        Exception: If an error occurs while saving the user to the database.
        400: If there is an error processing the user data.
    """

    user_logic = UserLogic()

    new_user = user_logic.save_user(request.json)

    if not new_user:
        return jsonify({"message": "Error al guardar el usuario"}), 400

    return jsonify(new_user), 201


# edicion usuario
@bp.route("/usuarios/<id>", methods=["PATCH"])
@token_required
@require_json
@handle_api_exceptions(default_message="Error al actualizar el usuario")
def update_user(id):
    """
    Updates an existing user.
    Args:
        id (int): The ID of the user to update.
    Returns:
        Response: A JSON with the updated user's data.
    Raises:
        ValueError: If the user is not found or required fields are missing.
        SQLAlchemyError: If there is an error updating the user in the database.
        Exception: For any other exception that occurs.
    """

    if not id:
        return jsonify({"message": "No se proporcionó el ID del usuario"}), 400

    user_logic = UserLogic()

    user_to_update = user_logic.update_user(id, request.json)

    if not user_to_update:
        return jsonify({"message": "Error al actualizar el usuario"}), 400

    return jsonify({"message": "Usuario actualizado correctamente"}), 200


# eliminacion usuario
@bp.route("/usuarios/<id>", methods=["DELETE"])
@token_required
@handle_api_exceptions(default_message="Error al eliminar el usuario")
def delete_user(id):
    """
    Deletes a user by their ID.
    Args:
        id (int): The ID of the user to delete.
    Returns:
        Response: A JSON with the result of the deletion.
    Raises:
        ValueError: If the user with the provided ID is not found.
        Exception: If an error occurs while deleting the user.
        404: If the user is not found.
    """

    if not id:
        return jsonify({"message": "No se proporcionó el ID del usuario"}), 400

    user_logic = UserLogic()

    user_to_delete = user_logic.delete_user(id)

    if not user_to_delete:
        return jsonify({"message": "Error al eliminar el usuario"}), 400

    return jsonify({"message": "Usuario eliminado correctamente"}), 200
