from datetime import datetime
import json

from flask import Blueprint, request, jsonify

from src.utils.decorators import token_required

from ..models.models import Student, Tutor, db

from ..models.schemas import StudentSchema, TutorSchema

bp = Blueprint('alumnos', __name__)

# Definición de atajos de serializador
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)

# Definicion endpoint obtiene todos los alumnos
@bp.route('/alumnos', methods=['GET'])
@token_required
def getStudents():

    try:
        allStudents = Student.query.filter(Student.active == True).order_by(Student.id)
        
    except:
        return jsonify({"message":"No se pudieron obtener alumnos"}), 404
    
    if not allStudents:
        return jsonify({"message":"No se pueden obtener los alumnos"}), 400

    serialized_students = [student.as_dict() for student in allStudents]

    return jsonify(serialized_students), 200


# Definicion endpoint obtiene un solo alumno filtrado por id
@bp.route('/alumnos/<id>', methods=['GET'])
@token_required
def getStudentById(id):
    
    try:
        foundStudent = Student.query.get(id)

        if not foundStudent:
            return jsonify({"message":"Alumno no encontrado"}), 404
    
    except:
        return jsonify({"message":"No se pudo obtener el alumno"}), 404

    serialized_student = student_schema.dump(foundStudent)

    return jsonify(serialized_student), 200


# Definicion endpoint 'borra' un alumno, cambia el activo
@bp.route('/alumnos/<id>', methods=['DELETE'])
@token_required
def deteleStudent(id):
    try:
        foundStudent = Student.query.get(id)
    except:
        return jsonify({"message":"No se pudo obtener el alumno"}), 404
    
    try:
        foundStudent.active = False
        foundStudent.updatedAt = datetime.now
        db.session.commit()

    except:
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({"message":"No se pudo modificar el alumno"}), 204

    serialized_student = student_schema.dump(foundStudent)

    response_data = json.dumps(serialized_student, ensure_ascii=False)

    return jsonify(response_data), 201


# Definicionn endpoint creacion alumno
@bp.route('/alumnos', methods=['POST'])
@token_required
def saveStudent():

    newStudent = None

    if not request.json:
        return jsonify({'message': 'JSON data is missing or invalid'}), 400

    try:
        newStudent = Student(
            dni= request.json['dni'],
            names= request.json['names'],
            surnames= request.json['surnames'],
            address= request.json['address'],
            email = request.json['email'],
            active = request.json['active']
            )

    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    
    
    try:
       db.session.add(newStudent)
    except:
        return jsonify({'message':'No se pudo ADD alumno'}), 400
    
    try:
        # Confirmación de las operaciones creadas en la session
        db.session.commit()
        return jsonify({'message':'Success'}), 201
    
    except:
        return jsonify({'message':'No se puede commit'}), 400


# Definicionn endpoint edicion alumno
@bp.route('/alumnos/<id>', methods=['PATCH'])
@token_required
def updateStudent(id):
    try:
        foundStudent = Student.query.get(id)
    except:
        return jsonify({"message":"No se pudo obtener el alumno"}), 404
    
    if not foundStudent:
        return jsonify({"message":"No se pudo obtener el alumno"}), 404
    
    try:
        data = request.get_json()
    except:
        return jsonify({"message":"No hay información para actualizar el alumno"}), 404
    
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
        return jsonify({"message": "Error al modificar los campos del alumno: " + str(e)}), 500
    
    serialized_student = student_schema.dump(foundStudent)

    response_data = json.dumps(serialized_student, ensure_ascii=False)

    return jsonify(response_data), 201


# Definición endpoint para asociar tutores al alumno
@bp.route('/alumnos/<int:alumno_id>/tutores/<int:tutor_id>', methods=['POST'])
@token_required
def associate_tutor_with_student(alumno_id, tutor_id):
    try:
        # Buscar el estudiante y el tutor en la base de datos
        student = Student.query.get(alumno_id)
        tutor = Tutor.query.get(tutor_id)
        
        if not student or not tutor:
            return jsonify({"message":"No se encontró el estudiante o el tutor"}), 404
        
        # Verificar si la relación ya existe
        if tutor in student.tutors:
            return jsonify({"message":"La relación entre el estudiante y el tutor ya existe"}), 400
        
        # Asociar el tutor con el estudiante
        student.tutors.append(tutor)
        db.session.commit()
        
        return jsonify({"message":"La relación entre el estudiante y el tutor se ha establecido con éxito"}), 200
    
    except Exception as e:
        return jsonify({"message": "Error al asociar el tutor con el estudiante: " + str(e)}), 500