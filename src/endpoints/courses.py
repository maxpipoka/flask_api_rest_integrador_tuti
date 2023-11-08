from datetime import datetime

from flask import Response, Blueprint, request, jsonify

from ..models.models import Course, db

bp = Blueprint('cursos', __name__)

# Definicion endpoint obtiene todos los cursos
@bp.route('/cursos', methods=['GET'])
def getAllCourses():

    try:
        allCourses = Course.query.filter(Course.active == True)

    except:
        return Response({'message':'No se pudieron obtener los cursos'}), 404
    
    if not allCourses:
        return Response({'message':'No se pueden obtener los cursos'}), 400
    
    serialized_courses = [course.as_dict() for course in allCourses]

    return jsonify(serialized_courses), 200


# Definicion endpoint obtiene un solo curso filtrado por id
@bp.route('/cursos/<id>', methods=['GET'])
def getOneCourse(id):
    
    try:
        foundCourse = Course.query.get(id)

    except:
        return Response({'message': 'No se pudo obtener el curso'}), 404
    
    if not foundCourse:
        return Response({'message':'El curso no existe'}), 400
    
    serialized_course = [foundCourse.as_dict()]

    return jsonify(serialized_course), 200


# Definicion endpoint 'borra' un curso, cambio el activo
@bp.route('/cursos/', methods=['DELETE'])
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

        print(newCourse)

    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    

    try:
        db.session.add(newCourse)

    except:
        return jsonify({'message':'No se pudo ADD curso'}), 400
    
    try:
        # Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        return Response({'message': 'success'}), 201

    except:
        return Response({'message': 'No se puede commit'}), 400
    


# Definicion endpoint edicion curso
@bp.route('/cursos/<id>', methods=['PATCH'])
def editCourse(id):

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