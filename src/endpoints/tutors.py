from datetime import datetime
import json

from flask import Response, Blueprint, request, jsonify

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from src.utils.decorators import handle_logic_exceptions, token_required, require_json

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
@handle_logic_exceptions(default_message="Error al obtener los tutores activos")
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
@handle_logic_exceptions(default_message="Error al eliminar el tutor")
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
@handle_logic_exceptions(default_message="Error al guardar el tutor")
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
def update_tutor(id):
    try:
        founded_tutor = db.session.get(Tutor, id)
        
    except:
        return jsonify({"message":"No se pudo obtener el tutor"}), 404
    
    if not founded_tutor:
        return jsonify({"message":"No se pudo obtener el tutor"}), 404
    
    try:
        data = request.get_json()
    except:
        return jsonify({"message":"No hay información para actualizar el tutor"}), 400
    
    try:
        updated = False

        if 'names' in data:
            founded_tutor.names = data['names']
            updated = True

        if 'surnames' in data:
            founded_tutor.surnames = data['surnames']
            updated = True

        if 'address' in data:
            founded_tutor.address = data['address']
            updated = True

        if 'email' in data and data['email']:
            founded_tutor.email = data['email']
            updated = True

        if 'active' in data:
            founded_tutor.active = data['active']
            updated = True

        if 'student_id' in data:
            founded_tutor.student_id = data['student_id']
            updated = True

        if updated:
            founded_tutor.updated_at = datetime.now()

        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({"message": "Error al modificar los campos del tutor: " + str(e)}), 500
    
    serialized_tutor = tutor_schema.dump(founded_tutor)

    # response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(serialized_tutor), 201