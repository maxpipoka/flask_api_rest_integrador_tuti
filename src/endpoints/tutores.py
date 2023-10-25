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


# Definicion endpoint que borra un alumno, cambia el activo
@bp.route('/tutores/<id>', methods=['DELETE'])
def deleteOneTutor(id):
    try:
        foundedTutor = Tutor.query.get(id)
    except:
        pass