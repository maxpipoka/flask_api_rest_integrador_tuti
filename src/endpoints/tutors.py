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
def getTutors():
    try:
        allTutors = Tutor.query.filter(Tutor.active == True).order_by(Tutor.id)
    except:
        return jsonify({"message": "No se puede obtener los tutores"}), 404
    
    if not allTutors:
        return jsonify({"message": "No se pueden obtener los tutores"}), 400
    
    serialized_tutors = [tutor.as_dict() for tutor in allTutors]


    return jsonify(serialized_tutors), 200


# Definición endpoint obtiene un solo alumno filtrado por id
@bp.route('/tutores/<id>', methods=['GET'])
@token_required
def getTutorById(id):
    try:
        foundedTutor = Tutor.query.get(id)
    except:
        return jsonify({"message":"No se puede obtener el tutor"}), 400
    
    serialized_tutor = tutor_schema.dump(foundedTutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(response_data), 200


# Definicion endpoint que borra un tutor, cambia el activo
@bp.route('/tutores/<id>', methods=['DELETE'])
@token_required
def deleteTutor(id):
    try:
        foundedTutor = Tutor.query.get(id)
    except:
        return jsonify({"message": "No se puede obtener el tutor"}), 404
    
    try:
        foundedTutor.active = False
        foundedTutor.updatedAt = datetime.now()
        db.session.commit()
        
    except:
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({"message":"No se pudo borrar el tutor"}), 400
    
    serialized_tutor = tutor_schema.dump(foundedTutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(response_data), 200


# Definicion endpoint creacion tutor
@bp.route('/tutores', methods=['POST'])
@token_required
def saveTuror():
    newTutor = None

    if not request.json:
        return jsonify({'message': 'JSON data is missing or invalid'}), 400

    try:
        newTutor = Tutor(
            dni= request.json['dni'],
            names= request.json['names'],
            surnames= request.json['surnames'],
            address= request.json['address'],
            email= request.json['email'],
            active=request.json['active'],
            student_id=request.json['student_id']
            )
    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    
    try:
        db.session.add(newTutor)
    except:
        return jsonify({'message':'No se pudo ADD tutor'}), 400
    
    try:
        #Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        return jsonify({'message':'Success'}), 201
    except:
        return jsonify({'message':'No se puede commit'}), 400
    

@bp.route('/tutores/<id>', methods=['PATCH'])
@token_required
def updateTutor(id):
    try:
        foundTutor = Tutor.query.get(id)
        
    except:
        return jsonify({"message":"No se pudo obtener el tutor"}), 404
    
    if not foundTutor:
        return jsonify({"message":"No se pudo obtener el tutor"}), 404
    
    try:
        data = request.get_json()
    except:
        return jsonify({"message":"No hay información para actualizar el tutor"}), 400
    
    try:
        updated = False

        if 'names' in data:
            foundTutor.names = data['names']
            updated = True

        if 'surnames' in data:
            foundTutor.surnames = data['surnames']
            updated = True

        if 'address' in data:
            foundTutor.address = data['address']
            updated = True

        if 'email' in data and data['email']:
            foundTutor.email = data['email']
            updated = True

        if 'active' in data:
            foundTutor.active = data['active']
            updated = True

        if 'student_id' in data:
            foundTutor.student_id = data['student_id']
            updated = True

        if updated:
            foundTutor.updatedAt = datetime.now()

        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({"message": "Error al modificar los campos del tutor: " + str(e)}), 500
    
    serialized_tutor = tutor_schema.dump(foundTutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return jsonify(response_data), 201