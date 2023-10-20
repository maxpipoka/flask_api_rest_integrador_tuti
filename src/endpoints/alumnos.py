import json

from flask import Response, Blueprint

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
        allStudents = Student.query.all()
    except:
        return Response({"message":"No se pudieron obtener alumnos"}), 204
    
    if (allStudents == None):
        return Response({"message":"No existen alumnos"}), 200

    serialized_students = students_schema.dump(allStudents)

    response_data = json.dumps(serialized_students, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicion endpoint obtiene un solo alumno filtrado por id
@bp.route('/alumnos/<id>', methods=['GET'])
def getOneAlumno(id):
    try:
        findedStudent = Student.query.filter(Student.id == id)
    except:
        return Response({"message":"No se pudo obtener el alumno"}), 204
    
    if (findedStudent == None):
        return Response({"message":"El alumno no existe"}), 200

    serialized_students = students_schema.dump(findedStudent)

    response_data = json.dumps(serialized_students, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


# Definicion endpoint 'borra' un alumno, cambia el activo
@bp.route('/alumnos/borrar/<id>', methods=['DELETE'])
def deteleOneAlumno(id):
    try:
        findedStudent = Student.query.filter(Student.id == id)
    except:
        return Response({"message":"No se pudo obtener el alumno"}), 204

    serialized_students = students_schema.dump(findedStudent)

    response_data = json.dumps(serialized_students, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200


#Para guardar objetos se usa add_all