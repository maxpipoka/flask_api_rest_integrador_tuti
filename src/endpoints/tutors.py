from datetime import datetime
import json

from flask import Response, Blueprint, request, jsonify

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from src.utils.decorators import handle_logic_exceptions, token_required, require_json, handle_api_exceptions

from ..models.models import Tutor, db

from ..models.schemas import TutorSchema

from bussiness_logic.tutor_logic import TutorLogic

bp = Blueprint('tutores', __name__)

# Definición de atajos de serializador
tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)

# Definicion endpoint obtiene todos los tutores activos
@bp.route('/tutores', methods=['GET'])
@token_required
@handle_api_exceptions(default_message="Error al obtener los tutores activos")
def get_tutors():
    """
    Endpoint para obtener todos los tutores activos.
    Returns:
        JSON: Una lista de tutores activos.
    Raises:
        ValueError: Si no se encuentran tutores activos.
        SQLAlchemyError: Si hay un error al consultar la base de datos.
        Exception: Para cualquier otra excepción que ocurra.
    """
    
    tutor_logic = TutorLogic()

    all_active_tutors = tutor_logic.get_tutors()

    return jsonify(all_active_tutors), 200
    


# Definición endpoint obtiene un solo tutor filtrado por id
@bp.route('/tutores/<id>', methods=['GET'])
@token_required
def get_tutor_by_id(id):
    """
    Endpoint para obtener un tutor por su ID.
    Args:
        id (int): El ID del tutor a obtener.
    Returns:
        JSON: Un diccionario que representa el tutor encontrado.
    Raises:
        ValueError: Si no se encuentra el tutor con el ID proporcionado.
        SQLAlchemyError: Si hay un error al consultar la base de datos.
        Exception: Para cualquier otra excepción que ocurra.
    """

    tutor_logic = TutorLogic()

    founded_tutor = tutor_logic.get_tutor_by_id(id)

    return jsonify(founded_tutor.as_dict()), 200


# Definicion endpoint que borra un tutor, cambia el activo
@bp.route('/tutores/<id>', methods=['DELETE'])
@token_required
@handle_api_exceptions(default_message="Error al eliminar el tutor")
def delete_tutor(id):
    """ Endpoint para eliminar un tutor por su ID.
    Args:
        id (int): El ID del tutor a eliminar.
    Returns:
        JSON: Un mensaje de éxito o error.
    Raises:
        ValueError: Si no se encuentra el tutor con el ID proporcionado.
        SQLAlchemyError: Si hay un error al consultar la base de datos.
        Exception: Para cualquier otra excepción que ocurra.
    """

    tutor_logic = TutorLogic()

    tutor_to_delete = tutor_logic.delete_tutor(id)

    return jsonify(tutor_to_delete.as_dict()), 200


# Definicion endpoint creacion tutor
@bp.route('/tutores', methods=['POST'])
@token_required
@require_json
@handle_api_exceptions(default_message="Error al guardar el tutor")
def save_tutor():
    """
    Endpoint para crear un nuevo tutor.
    Returns:
        JSON: El tutor creado.
    Raises:
        ValueError: Si hay un error al crear el tutor o si los datos son inválidos
        SQLAlchemyError: Si hay un error al consultar la base de datos.
        Exception: Para cualquier otra excepción que ocurra.
    """

    tutor_logic = TutorLogic()

    new_tutor = tutor_logic.save_tutor(tutor_data=request.json)

    return jsonify(new_tutor.as_dict()), 201

    
    
# Deficion endpoint edicion tutor
@bp.route('/tutores/<id>', methods=['PATCH'])
@token_required
@require_json
@handle_api_exceptions(default_message="Error al actualizar el tutor")
def update_tutor(id):
    """
    Endpoint para actualizar un tutor por su ID.
    Args:
        id (int): El ID del tutor a actualizar.
    Returns:
        JSON: El tutor actualizado.
    Raises:
        ValueError: Si no se encuentra el tutor con el ID proporcionado o si no se
        hay datos para actualizar.
        SQLAlchemyError: Si hay un error al consultar la base de datos.
        Exception: Para cualquier otra excepción que ocurra.
    """

    if not id:
        return jsonify({"message": "ID del tutor es requerido"}), 400
    
    tutor_logic = TutorLogic()

    tutor_to_update = tutor_logic.update_tutor(id, tutor_data=request.json)
        
    return jsonify(tutor_to_update), 201