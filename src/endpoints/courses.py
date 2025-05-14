from datetime import datetime

from flask import Blueprint, request, jsonify

from src.utils.decorators import token_required

from ..models.models import Course, Student, db

bp = Blueprint('cursos', __name__)

# Definicion endpoint obtiene todos los cursos
@bp.route('/cursos', methods=['GET'])
@token_required
def get_courses():

    try:
        all_courses = Course.query.order_by(Course.level, Course.year, Course.division)

    except:
        return jsonify({'message':'No se pueden obtener los cursos'}), 404
    
    if not all_courses:
        return jsonify({'message':'No se pueden obtener los cursos'}), 400
    
    serialized_courses = [course.as_dict() for course in all_courses]

    return jsonify(serialized_courses), 200


# Definicion endpoint que obtiene todos los cursos bajo el control
# de un usuario específico (Preceptor)
@bp.route('/cursos/preceptor/<int:preceptor_id>', methods=['GET'])
@token_required
def get_courses_by_preceptor(preceptor_id):
    
    try:
        founded_courses = Course.query.filter(Course.associated_user == preceptor_id).filter(Course.active == True).filter(Course.current == True).order_by(Course.level, Course.year, Course.division)

    except:
        return jsonify({'message':'No se puede obtener los cursos'}), 404
    
    if not founded_courses:
        return jsonify({'message':'No se encontraron cursos'}), 404
    
    
    serialized_courses = [course.as_dict() for course in founded_courses]

    return jsonify(serialized_courses), 200


# Definicion endpoint obtiene un solo curso filtrado por id
@bp.route('/cursos/<id>', methods=['GET'])
@token_required
def get_course_by_id(id):
    
    try:
        founded_course = db.session.get(Course, id)

    except:
        return jsonify({'message': 'No se pudo obtener el curso'}), 404
    
    if not founded_course:
        return jsonify({'message':'El curso no existe'}), 404
    
    serialized_course = founded_course.as_dict()

    return jsonify(serialized_course), 200


# Definicion endpoint 'borra' un curso, cambio del activo
@bp.route('/cursos/<int:id>', methods=['DELETE'])
@token_required
def delete_course(id):

    try:
        founded_course = db.session.get(Course, id)

    except:
        return jsonify({'message':'No se pudo obtener el curso'}), 404
    
    try:
        founded_course.active = False
        founded_course.updated_at = datetime.now()
        db.session.commit()

    except:
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({'message':'No se pudo borrar el curso'}), 404
    
    serialized_course = [founded_course.as_dict()]

    return jsonify(serialized_course), 201


# Definicion endpoint asignacion de alumno al curso
@bp.route('/cursos/<int:course_id>/alumno/<int:student_id>', methods=['POST'])
@token_required
def asociate_student_to_course(course_id, student_id):
    
    try:
        # Busqueda de las instancias
        founded_student = db.session.get(Student, student_id)
        founded_course = db.session.get(Course, course_id)

    except:
        return jsonify({'message':'No se pueden encontrar las instancias'}), 404
    
    
    if not founded_student or not founded_course:
        return jsonify({'message':'Estudiante o Curso son invalidos'}), 404


    for student_in in founded_course.students:
        if founded_student.id == student_in.id:
            return jsonify({'message':'El alumno ya se encuentra asignado'}), 400
    
    try:
        # Asociación del alumno con el curso
        founded_course.students.append(founded_student)
        db.session.commit()

    except Exception as e:
        print(f"Error during transaction: {str(e)}")
        db.session.rollback()
        return jsonify({'message':'No se pudo asignar el alumno al curso'}), 400
    
    return jsonify({'message':'La asociación del alumno con el curso se realizó con éxito'}), 200


# Definicion endpoint creacion curso
@bp.route('/cursos', methods=['POST'])
@token_required
def save_course():

    new_course = None

    if not request.json:
        return jsonify({'message':'JSON data is missing of invalid'}), 400
    
    try:
        new_course = Course(
            level = request.json['level'],
            division = request.json['division'],
            year = request.json['year'],
            current = request.json['current'],
            active = request.json['active'],
            associated_user = request.json['associated_user']
        )

    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    

    try:
        db.session.add(new_course)

    except:
        return jsonify({'message':'No se pudo agregar el curso'}), 400
    
    try:
        # Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        return jsonify({'message': 'success'}), 201

    except:
        return jsonify({'message': 'No se puede commit'}), 400
    

# Definicion endpoint edicion curso
@bp.route('/cursos/<id>', methods=['PATCH'])
@token_required
def update_course(id):

    try:
        founded_course = db.session.get(Course, id)

    except Exception as error:
        return jsonify({'message': f'No se puede obtener el curso - {str(error)}'}), 404
    
    if not founded_course:
        return jsonify({'message': 'No se puede obtener el curso'}), 404
    
    try:
        data = request.get_json()

    except Exception as error:
        return jsonify({'message':f'No hay informacipon para actualizar el curso - {str(error)}'}), 400
    
    try:
        updated = False

        if 'level' in data:
            founded_course.level = data['level']
            updated = True

        if 'division' in data:
            founded_course.division = data['division']
            updated = True

        if 'year' in data:
            founded_course.year = data['year']
            updated = True

        if 'current' in data:
            founded_course.current = data['current']
            updated = True

        if 'active' in data:
            founded_course.active = data['active']
            updated = True

        if 'associated_user' in data:
            founded_course.associated_user = data['associated_user']
            updated = True

        if updated:
            founded_course.updated_at = datetime.now()


        db.session.commit()

    except Exception as error:
        db.session.rollback() # Reversion transaccion
        return jsonify({'message':'Error al modificar los campos del curso: ' + str(error)}), 500
    
    serialized_course = founded_course.as_dict()

    return jsonify(serialized_course), 201