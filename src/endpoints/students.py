from flask import Blueprint, request, jsonify

from src.utils.decorators import require_json, token_required, handle_logic_exceptions

from ..models.schemas import StudentSchema, TutorSchema

from bussiness_logic.student_logic import StudentLogic

bp = Blueprint("alumnos", __name__)

# Definición de atajos de serializador
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)


# Definicion endpoint obtiene todos los alumnos ACTIVOS
@bp.route("/alumnos", methods=["GET"])
@token_required
@handle_logic_exceptions(default_message="Error al obtener los estudiantes activos")
def get_students():
    """
    Endpoint to get all active students.
    Returns:
        JSON: A list of active students.
    Raises:
        ValueError: If no active students are found.
    """

    student_logic = StudentLogic()

    all_active_students = student_logic.get_studentes()

    return jsonify(all_active_students), 200


# Definicion endpoint obtiene todos los alumnos, ACTIVOS e INACTIVOS
@bp.route("/alumnos/todos", methods=["GET"])
@token_required
@handle_logic_exceptions(default_message="Error al obtener todos los estudiantes")
def get_all_students():
    """
    Endpoint to get all students, both active and inactive.
    Returns:
        JSON: A list of all students.
    Raises:
        ValueError: If no students are found.
    """

    student_logic = StudentLogic()

    all_students = student_logic.get_all_students

    return jsonify(all_students), 200


# Definicion endpoint obtiene un solo alumno filtrado por id
@bp.route("/alumnos/<id>", methods=["GET"])
@token_required
@handle_logic_exceptions(default_message="Error al obtener el alumno")
def get_student_by_id(id):
    """
    Endpoint to get a student by their ID.
    Args:
        id (int): The ID of the student to fetch.
    Returns:
        JSON: The student object if found.
    Raises:
        ValueError: If the student with the given ID is not found.
    """

    if not id:
        return jsonify({"message": "ID del alumno es requerido"}), 400

    student_logic = StudentLogic()

    founded_student = student_logic.get_student_by_id(id)

    return jsonify(founded_student), 200


# Definicion endpoint 'borra' un alumno, cambia el activo
@bp.route("/alumnos/<id>", methods=["DELETE"])
@token_required
@handle_logic_exceptions(default_message="Error al eliminar el alumno")
def detele_student(id):
    """
    Endpoint to delete a student by their ID.
    Args:
        id (int): The ID of the student to delete.
    Returns:
        JSON: The deleted student object if successful.
    Raises:
        Exception: If the student with the given ID is not found or if there is an error during deletion.
    """

    if not id:
        return jsonify({"message": "ID del alumno es requerido"}), 400

    student_logic = StudentLogic()

    founded_student = student_logic.delete_student_by_id(id)

    return jsonify(founded_student), 201


# Definicionn endpoint creacion alumno
@bp.route("/alumnos", methods=["POST"])
@token_required
@require_json
@handle_logic_exceptions(default_message="Error al crear el alumno")
def save_student():
    """
    Endpoint to create a new student.
    Returns:
        JSON: The created student object.
    Raises:
        ValueError: If required fields are missing in the student data.
        IntegrityError: If there is a database integrity error (e.g., unique constraint violation).
        Exception: For any other exceptions that occur.
    """

    student_logic = StudentLogic()

    new_student = student_logic.save_student(student_data=request.json)

    return jsonify(new_student), 201


# Definicionn endpoint edicion alumno
@bp.route("/alumnos/<id>", methods=["PATCH"])
@token_required
@require_json
@handle_logic_exceptions(default_message="Error al actualizar el alumno")
def update_student(id):
    """
    Endpoint to update an existing student by their ID.
    Args:
        id (int): The ID of the student to update.
    Returns:
        JSON: The updated student object if successful.
    Raises:
        ValueError: If the student with the given ID is not found or if required fields are missing in the update data.
        IntegrityError: If there is a database integrity error (e.g., unique constraint violation).
        Exception: For any other exceptions that occur.
    """

    if not id:
        return jsonify({"message": "ID del alumno es requerido"}), 400

    student_logic = StudentLogic()

    updated_student = student_logic.update_student(id, student_data=request.json)

    return jsonify(updated_student), 200


# Definición endpoint para asociar tutores al alumno
@bp.route("/alumnos/<int:alumno_id>/tutores/<int:tutor_id>", methods=["POST"])
@token_required
@handle_logic_exceptions(default_message="Error al asociar el tutor con el estudiante")
def associate_tutor_with_student(student_id, tutor_id):
    """
    Endpoint to associate a tutor with a student.
    Args:
        alumno_id (int): The ID of the student to associate with a tutor.
        tutor_id (int): The ID of the tutor to associate with the student.
    Returns:
        JSON: The associated student object with the tutor.
    Raises:
        ValueError: If the student ID or tutor ID is not provided.
        IntegrityError: If there is a database integrity error (e.g., unique constraint violation).
        Exception: For any other exceptions that occur.
    """

    if not student_id or not tutor_id:
        return jsonify({"message": "ID del alumno y del tutor son requeridos"}), 400

    student_logic = StudentLogic()

    associated_student = student_logic.associate_tutor_with_student(
        student_id=student_id, tutor_id=tutor_id
    )

    return jsonify(associated_student), 200
