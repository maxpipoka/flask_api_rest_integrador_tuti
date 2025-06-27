from flask import Blueprint, jsonify, request

from src.utils.decorators import token_required, handle_api_exceptions

from bussiness_logic.auth_logic import AuthLogic

bp = Blueprint("auth", __name__)


# Definicion endpoint que realiza verificacion de existencia de la url
@bp.route("/auth", methods=["GET"])
def test_auth():
    return jsonify({"message": "Endpoint de autenticación"}), 200


# Definicion endpoint realiza la autenticación de un usuario
@bp.route("/auth", methods=["POST"])
@handle_api_exceptions(default_message="Error during user login")
def login_user():

    if (
        not request.is_json
        or "username" not in request.json
        or "password" not in request.json
    ):
        return jsonify({"message": "Required data not provided"}), 400

    auth_logic = AuthLogic()

    founded_user = auth_logic.login_user(request.json)

    return jsonify(founded_user), 200


# Definicion endpoint realiza el registro de un usuario
@bp.route("/auth/register", methods=["POST"])
@token_required
@handle_api_exceptions(default_message="Error during user registration")
def register_user():

    if (
        not request.is_json
        or "username" not in request.json
        or "password" not in request.json
        or "fullname" not in request.json
        or "rol" not in request.json
        or "access_level" not in request.json
    ):
        return jsonify({"message": "Required data not provided"}), 400

    auth_logic = AuthLogic()

    new_user = auth_logic.register_user(request.json)
    if "message" in new_user:
        return jsonify(new_user), 201
