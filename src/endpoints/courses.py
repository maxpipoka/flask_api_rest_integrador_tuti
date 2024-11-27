from datetime import datetime

from flask import Response, Blueprint, request, jsonify

from ..models.models import Course, Student, db

bp = Blueprint('cursos', __name__)

# Definicion endpoint obtiene todos los cursos
@bp.route('/cursos', methods=['GET'])
def getCourses():

    try:
        allCourses = Course.query.filter(Course.active == True).order_by(Course.id)

    except:
        return Response({'message':'No se pueden obtener los cursos'}), 404
    
    if not allCourses:
        return Response({'message':'No se pueden obtener los cursos'}), 400
    
    serialized_courses = [course.as_dict() for course in allCourses]

    return jsonify(serialized_courses), 200


# Definicion endpoint que obtiene todos los cursos bajo el control
# de un usuario específico (Preceptor)
@bp.route('/cursos/preceptor/<int:preceptor_id>', methods=['GET'])
def getCoursesByPreceptor(preceptor_id):
    
    try:
        foundedCourses = Course.query.filter(Course.associated_user == preceptor_id).all()

    except:
        return Response({'message':'No se puede obtener los cursos'}), 404
    
    if not foundedCourses:
        return Response({'message':'No se encontraron cursos'}), 400
    
    
    serialized_courses = [course.as_dict() for course in foundedCourses]

    return jsonify(serialized_courses), 200


# Definicion endpoint obtiene un solo curso filtrado por id
@bp.route('/cursos/<id>', methods=['GET'])
def getCourseById(id):
    
    try:
        foundCourse = Course.query.get(id)

    except:
        return Response({'message': 'No se pudo obtener el curso'}), 404
    
    if not foundCourse:
        return Response({'message':'El curso no existe'}), 400
    
    serialized_course = foundCourse.as_dict()

    return jsonify(serialized_course), 200


# Definicion endpoint 'borra' un curso, cambio el activo
@bp.route('/cursos/<int:id>', methods=['DELETE'])
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
def asociate_student_to_course(course_id, student_id):
    
    try:
        # Busqueda de las instancias
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)

    except:
        return Response({'message':'No se pueden encontrar las instancias'}), 400
    
    if not student or not course:
        return Response({'message':'Student o Course son invalidos'}), 400
    print(' ')
    print(course.students)
    print(' ')

    for studentIn in course.students:
        if student.id == studentIn.id:
            return Response({'message':'El alumno ya se encuentra asignado'}), 400
    
    try:
        # Asociación del alumno con el curso
        course.students.append(student)
        db.session.commit()

    except Exception as e:
        print(f"Error during transaction: {str(e)}")
        db.session.rollback()
        return Response({'message':'No se pudo asignar el alumno al curso'}), 400
    
    return Response({'message':'La asociación del alumno con el curso se realizó con éxito'}), 200

# Definicion endpoint creacion curso
@bp.route('/cursos', methods=['POST'])
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
            active = request.json['active']
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

        if updated:
            foundCourse.updatedAt = datetime.now()


        db.session.commit()

    except Exception as e:
        db.session.rollback() # Reversion transaccion
        return Response({'message':'Error al modificar los campos del curso: ' + str(e)}), 500
    
    serialized_course = foundCourse.as_dict()

    return jsonify(serialized_course), 200