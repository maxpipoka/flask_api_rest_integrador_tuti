from datetime import datetime

from flask import Response, Blueprint, request, jsonify

from src.utils.decorators import token_required

from ..models.models import Course, Student, db

bp = Blueprint('cursos', __name__)

# Definicion endpoint obtiene todos los cursos
@bp.route('/cursos', methods=['GET'])
@token_required
def getCourses():

    try:
        allCourses = Course.query.filter(Course.active == True).order_by(Course.level, Course.year, Course.division)

    except:
        return Response({'message':'No se pueden obtener los cursos'}), 404
    
    if not allCourses:
        return Response({'message':'No se pueden obtener los cursos'}), 400
    
    serialized_courses = [course.as_dict() for course in allCourses]

    return jsonify(serialized_courses), 200


# Definicion endpoint que obtiene todos los cursos bajo el control
# de un usuario específico (Preceptor)
@bp.route('/cursos/preceptor/<int:preceptor_id>', methods=['GET'])
@token_required
def getCoursesByPreceptor(preceptor_id):
    
    try:
        foundedCourses = Course.query.filter(Course.associated_user == preceptor_id).filter(Course.active == True).filter(Course.current == True).order_by(Course.level, Course.year, Course.division)

    except:
        return Response({'message':'No se puede obtener los cursos'}), 404
    
    if not foundedCourses:
        return Response({'message':'No se encontraron cursos'}), 400
    
    
    serialized_courses = [course.as_dict() for course in foundedCourses]

    return jsonify(serialized_courses), 200


# Definicion endpoint obtiene un solo curso filtrado por id
@bp.route('/cursos/<id>', methods=['GET'])
@token_required
def getCourseById(id):
    
    try:
        foundCourse = Course.query.get(id)

    except:
        return Response({'message': 'No se pudo obtener el curso'}), 404
    
    if not foundCourse:
        return Response({'message':'El curso no existe'}), 400
    
    serialized_course = foundCourse.as_dict()

    return jsonify(serialized_course), 200


# Definicion endpoint 'borra' un curso, cambio del activo
@bp.route('/cursos/<int:id>', methods=['DELETE'])
@token_required
def deleteCourse(id):

    try:
        foundCourse = Course.query.get(id)

    except:
        return Response({'message':'No se pudo obtener el curso'}), 404
    
    try:
        foundCourse.active = False
        foundCourse.updatedAt = datetime.now()
        db.session.commit()

    except:
        db.session.rollback()  # Revertir la transacción en caso de error
        return Response({'message':'No se pudo borrar el curso'}), 404
    
    serialized_course = [foundCourse.as_dict()]

    return jsonify(serialized_course), 201


# Definicion endpoint asignacion de alumno al curso
@bp.route('/cursos/<int:course_id>/alumno/<int:student_id>', methods=['POST'])
@token_required
def asociate_student_to_course(course_id, student_id):
    
    try:
        # Busqueda de las instancias
        foundedStudent = Student.query.get(student_id)
        foundedCourse = Course.query.get(course_id)

    except:
        return Response({'message':'No se pueden encontrar las instancias'}), 400
    
    if not foundedStudent or not foundedCourse:
        return Response({'message':'Estudiante o Curso son invalidos'}), 400


    for studentIn in foundedCourse.students:
        if foundedStudent.id == studentIn.id:
            return Response({'message':'El alumno ya se encuentra asignado'}), 400
    
    try:
        # Asociación del alumno con el curso
        foundedCourse.students.append(foundedStudent)
        db.session.commit()

    except Exception as e:
        print(f"Error during transaction: {str(e)}")
        db.session.rollback()
        return Response({'message':'No se pudo asignar el alumno al curso'}), 400
    
    return Response({'message':'La asociación del alumno con el curso se realizó con éxito'}), 200


# Definicion endpoint creacion curso
@bp.route('/cursos', methods=['POST'])
@token_required
def saveCourse():

    newCourse = None

    if not request.json:
        return Response({'message':'JSON data is missing of invalid'}), 400
    
    try:
        newCourse = Course(
            level = request.json['level'],
            division = request.json['division'],
            year = request.json['year'],
            current = request.json['current'],
            active = request.json['active'],
            associated_user = request.json['associated_user']
        )

    except KeyError as e:
        return jsonify({'message1': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message2': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message3':'No se puede crear la instancia'}), 400
    

    try:
        db.session.add(newCourse)

    except:
        return Response({'message':'No se pudo ADD curso'}), 400
    
    try:
        # Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        return Response({'message': 'success'}), 201

    except:
        return Response({'message': 'No se puede commit'}), 400
    

# Definicion endpoint edicion curso
@bp.route('/cursos/<id>', methods=['PATCH'])
@token_required
def updateCourse(id):

    try:
        foundCourse = Course.query.get(id)

    except:
        return Response({'message': 'No se puede obtener el curso'}), 400
    
    if not foundCourse:
        return Response({'message': 'No se puede obtener el curso'}), 400
    
    try:
        data = request.get_json()

    except:
        return Response({'message':'JSON data is missing or invalid'}), 400
    
    try:
        updated = False

        if 'level' in data:
            foundCourse.level = data['level']
            updated = True

        if 'division' in data:
            foundCourse.division = data['division']
            updated = True

        if 'year' in data:
            foundCourse.year = data['year']
            updated = True

        if 'current' in data:
            foundCourse.current = data['current']
            updated = True

        if 'active' in data:
            foundCourse.active = data['active']
            updated = True

        if 'associated_user' in data:
            foundCourse.associated_user = data['associated_user']
            updated = True

        if updated:
            foundCourse.updatedAt = datetime.now()


        db.session.commit()

    except Exception as e:
        db.session.rollback() # Reversion transaccion
        return Response({'message':'Error al modificar los campos del curso: ' + str(e)}), 500
    
    serialized_course = foundCourse.as_dict()

    return jsonify(serialized_course), 200