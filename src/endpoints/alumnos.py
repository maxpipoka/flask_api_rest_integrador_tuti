from datetime import datetime
import json

from flask import Response, Blueprint, request, jsonify

from ..models.models import Student, db

from .schemas import StudentSchema

bp = Blueprint('alumnos', __name__)

# Definición de atajos de serializador
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Definicion endpoint obtiene todos los alumnos
@bp.route('/alumnos', methods=['GET'])
def getAllAlumnos():

    try:
        allStudents = Student.query.filter(Student.active == True)
    except:
        return Response({"message":"No se pudieron obtener alumnos"}), 404
    
    if not allStudents:
        return Response({"message":"No se pueden obtener los alumnos"}), 400

    serialized_students = students_schema.dump(allStudents)

    response_data = json.dumps(serialized_students, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicion endpoint obtiene un solo alumno filtrado por id
@bp.route('/alumnos/<id>', methods=['GET'])
def getOneAlumno(id):
    try:
        foundStudent = Student.query.get(id)
    except:
        return Response({"message":"No se pudo obtener el alumno"}), 404
    
    if not foundStudent:
        return Response({"message":"El alumno no existe"}), 404

    serialized_student = student_schema.dump(foundStudent)

    response_data = json.dumps(serialized_student, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicion endpoint 'borra' un alumno, cambia el activo
@bp.route('/alumnos/<id>', methods=['DELETE'])
def deteleOneAlumno(id):
    try:
        foundStudent = Student.query.get(id)
    except:
        return Response({"message":"No se pudo obtener el alumno"}), 404
    
    try:
        foundStudent.active = False
        db.session.commit()
    except:
        return Response({"message":"No se pudo modificar el alumno"}), 204

    serialized_student = student_schema.dump(foundStudent)

    response_data = json.dumps(serialized_student, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicionn endpoint creacion alumno
@bp.route('/alumnos', methods=['POST'])
def createStudent():

    newStudent = None

    try:
        newStudent = Student(
            dni= request.json['dni'],
            names= request.json['names'],
            surnames= request.json['surnames'],
            address= request.json['address'],
            email = request.json['email'],
            active = request.json['active']
            )
        print(newStudent)

    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'messagedd': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    
    
    try:
       db.session.add(newStudent)
    except:
        return jsonify({'message':'No se puede ADD'}), 400
    
    try:
        # Confirmación de las operaciones creadas en la session
        db.session.commit()
        return jsonify({'message':'Success'}), 201
    except:
        return jsonify({'message':'No se puede commit'}), 400


@bp.route('/alumnos/<id>', methods=['PATCH'])
def editOneAlumno(id):
    try:
        foundStudent = Student.query.get(id)
    except:
        return Response({"message":"No se pudo obtener el alumno"}), 204
    
    if not foundStudent:
        return Response({"message":"No se pudo obtener el alumno"}), 404
    
    try:
        data = request.get_json()
    except:
        return Response({"message":"No hay información para actualizar el alumno"}), 404
    
    try:
        updated = False

        if 'names' in data:
            foundStudent.names = data['names']
            updated = True

        if 'surnames' in data:
            foundStudent.surnames = data['surnames']
            updated = True

        if 'address' in data:
            foundStudent.address = data['address']
            updated = True

        if 'email' in data and data['email']:
            foundStudent.email = data['email']
            updated = True

        if 'active' in data:
            foundStudent.active = data['active']
            updated = True

        if updated:
            foundStudent.updatedAt = datetime.now()

        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Revertir la transacción en caso de error
        return Response({"message": "Error al modificar los campos del alumno: " + str(e)}, status=500)
    
    serialized_student = student_schema.dump(foundStudent)

    response_data = json.dumps(serialized_student, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 201


