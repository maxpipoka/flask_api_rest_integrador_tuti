from datetime import datetime
import json

from flask import Response, Blueprint, request, jsonify

from src.utils.decorators import token_required

from ..models.models import Tutor, db

from ..models.schemas import TutorSchema

bp = Blueprint('tutores', __name__)

# Definición de atajos de serializador
tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)

# Definicion endpoint obtiene todos los tutores
@bp.route('/tutores', methods=['GET'])
@token_required
def get_tutors():
    try:
        all_tutors = Tutor.query.filter(Tutor.active == True).order_by(Tutor.id)
    except:
        return jsonify({"message": "No se puede obtener los tutores"}), 404
    
    if not all_tutors:
        return jsonify({"message": "No se pueden obtener los tutores"}), 400
    
    serialized_tutors = [tutor.as_dict() for tutor in all_tutors]


    return jsonify(serialized_tutors), 200


# Definición endpoint obtiene un solo tutor filtrado por id
@bp.route('/tutores/<id>', methods=['GET'])
@token_required
def get_tutor_by_id(id):
    try:
        founded_tutor = db.session.get(Tutor, id)
    except:
        return jsonify({"message":"No se puede obtener el tutor"}), 400
    
    serialized_tutor = tutor_schema.dump(founded_tutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(response_data), 200


# Definicion endpoint que borra un tutor, cambia el activo
@bp.route('/tutores/<id>', methods=['DELETE'])
@token_required
def delete_tutor(id):
    try:
        founded_tutor = db.session.get(Tutor, id)
    except:
        return jsonify({"message": "No se puede obtener el tutor"}), 404
    
    try:
        founded_tutor.active = False
        founded_tutor.updated_at = datetime.now()
        db.session.commit()
        
    except:
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({"message":"No se pudo borrar el tutor"}), 400
    
    serialized_tutor = tutor_schema.dump(founded_tutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(response_data), 200


# Definicion endpoint creacion tutor
@bp.route('/tutores', methods=['POST'])
@token_required
def save_turor():
    new_tutor = None

    if not request.json:
        return jsonify({'message': 'JSON data is missing or invalid'}), 400

    try:
        new_tutor = Tutor(
            dni= request.json['dni'],
            names= request.json['names'],
            surnames= request.json['surnames'],
            address= request.json['address'],
            email= request.json['email'],
            active=request.json['active'],
            )
    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    
    try:
        db.session.add(new_tutor)
    except:
        return jsonify({'message':'No se pudo ADD tutor'}), 400
    
    try:
        #Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        return jsonify({'message':'Success'}), 201
    except:
        return jsonify({'message':'No se puede commit'}), 400
    
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

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(response_data), 201