from datetime import datetime
import json

from flask import Response, Blueprint, request, jsonify

from ..models.models import Tutor, db

from .schemas import TutorSchema

bp = Blueprint('tutores', __name__)

# Definición de atajos de serializador
tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)

# Definicion endpoint obtiene todos los tutores
@bp.route('/tutores', methods=['GET'])
def getAllTutors():
    try:
        allTutors = Tutor.query.filter(Tutor.active == True)
    except:
        return Response({"message": "No se puede obtener los tutores"}), 400
    
    if not allTutors:
        return Response({"message": "No se pueden obtener los tutores"}), 400
    
    serialized_tutors = tutors_schema.dump(allTutors)

    response_data = json.dumps(serialized_tutors, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definición endpoint obtiene un solo alumno filtrado por id
@bp.route('/tutores/<id>', methods=['GET'])
def getOneTutor(id):
    try:
        foundedTutor = Tutor.query.get(id)
    except:
        return Response({"message":"No se puede obtener el tutor"}), 400
    
    serialized_tutor = tutor_schema.dump(foundedTutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicion endpoint que borra un tutor, cambia el activo
@bp.route('/tutores/<id>', methods=['DELETE'])
def deleteOneTutor(id):
    try:
        foundedTutor = Tutor.query.get(id)
    except:
        return Response({"message": "No se puede obtener el tutor"}), 400
    
    try:
        foundedTutor.active = False
        foundedTutor.updatedAt = datetime.now()
        db.session.commit()
    except:
        return Response({"message":"No se pudo borrar el tutor"}), 400
    
    serialized_tutor = tutor_schema.dump(foundedTutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicion endpoint creacion tutor
@bp.route('/tutores', methods=['POST'])
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
        print(request.json)
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
def editTutor(id):
    try:
        foundTutor = Tutor.query.get(id)
        print('-------tutor encontrado')
        print(foundTutor)
    except:
        return Response({"message":"No se pudo obtener el tutor"}), 204
    
    if not foundTutor:
        return Response({"message":"No se pudo obtener el tutor"}), 404
    
    try:
        data = request.get_json()
    except:
        return Response({"message":"No hay información para actualizar el tutor"}), 404
    
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
        return Response({"message": "Error al modificar los campos del tutor: " + str(e)}, status=500)
    
    serialized_tutor = tutor_schema.dump(foundTutor)

    response_data = json.dumps(serialized_tutor, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 201