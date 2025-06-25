from flask import Blueprint, request, jsonify

from src.utils.decorators import token_required, handle_api_exceptions
from bussiness_logic.course_logic import CourseLogic

bp = Blueprint("cursos", __name__)


# Definicion endpoint obtiene todos los cursos
@bp.route("/cursos", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving courses")
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

    course_logic = CourseLogic()

    all_courses = course_logic.get_courses()

    return jsonify(all_courses), 200


# Definicion endpoint que obtiene todos los cursos bajo el control
# de un usuario específico (Preceptor)
@bp.route("/cursos/preceptor/<int:preceptor_id>", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving courses by preceptor")
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
        return jsonify({"message": "El id del preceptor es invalido"}), 400

    course_logic = CourseLogic()

    founded_courses = course_logic.get_courses_by_preceptor(preceptor_id)

    return jsonify(founded_courses), 200


# Definicion endpoint obtiene un solo curso filtrado por id
@bp.route("/cursos/<id>", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving course by ID")
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
        return jsonify({"message": "El id del curso es invalido"}), 400

    course_logic = CourseLogic()

    founded_course = course_logic.get_course_by_id(id)

    return jsonify(founded_course), 200


# Definicion endpoint 'borra' un curso, cambio del activo
@bp.route("/cursos/<int:id>", methods=["DELETE"])
@token_required
@handle_api_exceptions(default_message="Error deleting course")
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
        return jsonify({"message": "El id del curso es invalido"}), 400

    course_logic = CourseLogic()

    founded_course = course_logic.delete_course(id)

    return jsonify({"message": founded_course}), 201


# Definicion endpoint asignacion de alumno al curso
@bp.route("/cursos/<int:course_id>/alumno/<int:student_id>", methods=["POST"])
@token_required
@handle_api_exceptions(default_message="Error associating student to course")
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
        return jsonify({"message": "El id del curso o del alumno es invalido"}), 400

    course_logic = CourseLogic()

    associated_student = course_logic.asociate_student_to_course(course_id, student_id)

    return jsonify({"message": associated_student}), 200


# Definicion endpoint creacion curso
@bp.route("/cursos", methods=["POST"])
@token_required
@handle_api_exceptions(default_message="Error saving course")
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
        return jsonify({"message": "JSON data is missing of invalid"}), 400

    course_logic = CourseLogic()

    new_course = course_logic.save_course(course_data=request.json)

    return jsonify(new_course), 201


# Definicion endpoint edicion curso
@bp.route("/cursos/<id>", methods=["PATCH"])
@token_required
@handle_api_exceptions(default_message="Error updating course")
def update_course(id):
    """
    Endpoint to update an existing course by its ID.
    Args:
        id (int): The ID of the course to update.
    Returns:
        JSON response with the updated course or an error message.
    Raises:
        ValueError: If the course does not exist or there is an error retrieving it.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not id:
        return jsonify({"message": "El id del curso es invalido"}), 400

    if not request.json:
        return jsonify({"message": "JSON data is missing of invalid"}), 400

    course_logic = CourseLogic()

    updated_course = course_logic.update_course(id_course=id, course_data=request.json)

    return jsonify(updated_course), 200
