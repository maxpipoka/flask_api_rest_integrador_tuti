from datetime import datetime

from flask import Blueprint, request, jsonify

from sqlalchemy import SQLAlchemyError

from src.utils.decorators import token_required
from bussiness_logic.course_logic import CourseLogic

from ..models.models import Course, Student, db

bp = Blueprint('cursos', __name__)

# Definicion endpoint obtiene todos los cursos
@bp.route('/cursos', methods=['GET'])
@token_required
def get_courses():
    """
    Endpoint to retrieve all courses.
    Returns:
        JSON response with a list of all courses or an error message.
    Raises:
        ValueError: If there is an error retrieving courses.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    try:

        course_logic = CourseLogic()

        all_courses = course_logic.get_courses()

        return jsonify(all_courses), 200
    
    except ValueError as e:
        return jsonify({'message': f'Error retrieving courses: {str(e)}'}), 404
    
    except Exception as e:
        return jsonify({'message': f'Error retrieving courses: {str(e)}'}), 500
    
    except SQLAlchemyError as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500


# Definicion endpoint que obtiene todos los cursos bajo el control
# de un usuario específico (Preceptor)
@bp.route('/cursos/preceptor/<int:preceptor_id>', methods=['GET'])
@token_required
def get_courses_by_preceptor(preceptor_id):
    """
    Endpoint to retrieve all courses associated with a specific preceptor.
    Args:
        preceptor_id (int): The ID of the preceptor.
    Returns:
        JSON response with a list of courses associated with the preceptor or an error message.
    Raises:
        ValueError: If there is an error retrieving courses.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not preceptor_id:
        return jsonify({'message':'El id del preceptor es invalido'}), 400
    
    try:
        course_logic = CourseLogic()

        founded_courses = course_logic.get_courses_by_preceptor(preceptor_id)

        return jsonify(founded_courses), 200

    except ValueError as e:
        return jsonify({'message': f'Error retrieving courses: {str(e)}'}), 404
    
    except SQLAlchemyError as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error retrieving courses: {str(e)}'}), 500
    

# Definicion endpoint obtiene un solo curso filtrado por id
@bp.route('/cursos/<id>', methods=['GET'])
@token_required
def get_course_by_id(id):
    """
    Endpoint to retrieve a course by its ID.
    Args:
        id (int): The ID of the course to retrieve.
    Returns:
        JSON response with the course details or an error message.
    Raises:
        ValueError: If there is an error retrieving the course.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not id:
        return jsonify({'message':'El id del curso es invalido'}), 400
    
    try:
        course_logic = CourseLogic()

        founded_course = course_logic.get_course_by_id(id)

        return jsonify(founded_course), 200

    except ValueError as e:
        return jsonify({'message': f'Error retrieving course: {str(e)}'}), 404
    
    except SQLAlchemyError as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error retrieving course: {str(e)}'}), 500
        


# Definicion endpoint 'borra' un curso, cambio del activo
@bp.route('/cursos/<int:id>', methods=['DELETE'])
@token_required
def delete_course(id):
    """
    Endpoint to delete a course by its ID, marking it as inactive.
    Args:
        id (int): The ID of the course to be deleted.
    Returns:
        JSON response with a success message or an error message.
    Raises:
        ValueError: If the course does not exist or there is an error retrieving it.
        SQLAlchemyError: If there is a database error. 
        Exception: For any other exceptions that occur.
    """

    if not id:
        return jsonify({'message':'El id del curso es invalido'}), 400

    try:
        course_logic = CourseLogic()

        founded_course = course_logic.delete_course(id)

        return jsonify({'message': founded_course}), 201

    except ValueError as e:
        return jsonify({'message': f'Error retrieving course: {str(e)}'}), 404
    
    except SQLAlchemyError as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error retrieving course: {str(e)}'}), 500
    


# Definicion endpoint asignacion de alumno al curso
@bp.route('/cursos/<int:course_id>/alumno/<int:student_id>', methods=['POST'])
@token_required
def asociate_student_to_course(course_id, student_id):
    """
    Endpoint to associate a student with a course.
    Args:
        course_id (int): The ID of the course.
        student_id (int): The ID of the student.
    Returns:
        JSON response with a success message or an error message.
    Raises:
        ValueError: If the course or student does not exist or there is an error retrieving them.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not course_id or not student_id:
        return jsonify({'message':'El id del curso o del alumno es invalido'}), 400
    
    try:
        course_logic = CourseLogic()
        associated_student = course_logic.asociate_student_to_course(course_id, student_id)
        return jsonify({'message': associated_student}), 200

    except ValueError as e:
        return jsonify({'message': f'Error associating student to course: {str(e)}'}), 404
    
    except SQLAlchemyError as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error associating student to course: {str(e)}'}), 500


# Definicion endpoint creacion curso
@bp.route('/cursos', methods=['POST'])
@token_required
def save_course():
    """
    Endpoint to create a new course.
    Returns:
        JSON response with the created course or an error message.
    Raises:
        ValueError: If the course data is invalid or there is an error saving it. 
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not request.json:
        return jsonify({'message':'JSON data is missing of invalid'}), 400
    
    try:

        course_logic = CourseLogic()
        new_course = course_logic.save_course(course_data=request.json)
        return jsonify(new_course), 201

    except ValueError as e:
        return jsonify({'message': f'Error saving course: {str(e)}'}), 400
    
    except SQLAlchemyError as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error saving course: {str(e)}'}), 500
    

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