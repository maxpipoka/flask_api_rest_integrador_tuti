from flask import Blueprint, request, jsonify

from bussiness_logic.attendance_logic import AttendanceLogic

from src.utils.decorators import token_required, require_json, handle_api_exceptions

bp = Blueprint("asistencias", __name__)


# Definicion endpoint obtiene las asistencias
@bp.route("/asistencias", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def get_attendances():
    """
    Endpoint to retrieve all active attendances.
    Returns:
        JSON response with a list of active attendances or an error message.
    Raises:
        ValueError: If there is an error retrieving attendances.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    attendance_logic = AttendanceLogic()

    active_attendances = attendance_logic.get_attendances()

    return jsonify(active_attendances), 200


# Definicion endpoint obtiene las asistencias inactivas
@bp.route("/asistencias/inactivas", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def get_inactive_attendances():
    """
    Endpoint to retrieve all inactive attendances.
    Returns:
        JSON response with a list of inactive attendances or an error message.
    Raises:
        ValueError: If there is an error retrieving inactive attendances.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    attendance_logic = AttendanceLogic()

    inactive_attendances = attendance_logic.get_inactive_attendances()

    return jsonify(inactive_attendances), 200


# Definicion endpoint obtencion una asistencia por id
@bp.route("/asistencias/<int:id>", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def get_attendance_by_id(id):
    """
    Endpoint to retrieve a specific attendance by its ID.
    Args:
        id (int): The ID of the attendance to retrieve.
    Returns:
        JSON response with the attendance details or an error message.
    Raises:
        ValueError: If there is an error retrieving the attendance.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not id:
        return jsonify({"message": "El id de la asistencia es invalido"}), 400

    attendance_logic = AttendanceLogic()

    founded_attendance = attendance_logic.get_attendance_by_id(id)

    return jsonify(founded_attendance), 200


# Definicion endpoint obtencion de asistencias por id de alumno
@bp.route("/asistencias/alumno/<int:id>", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def get_attendances_by_student_id(id):
    """
    Endpoint to retrieve all attendances for a specific student by their ID.
    Args:
        id (int): The ID of the student whose attendances are to be retrieved.
    Returns:
        JSON response with a list of attendances for the student or an error message.
    Raises:
        ValueError: If there is an error retrieving the attendances.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if "start" not in request.args or "end" not in request.args:
        return jsonify({"message": "Missing required date filters"}), 400

    if not id:
        return jsonify({"message": "El id del alumno es invalido"}), 400

    attendance_logic = AttendanceLogic()

    founded_attendances = attendance_logic.get_attendances_by_student_id(
        id, request_data=request.args
    )

    return jsonify(founded_attendances), 200


# Definicion endpoint para cerra asistencia de un curso en un dia
@bp.route("/asistencias/cerrar/<int:id>", methods=["POST"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def close_attendance(id):
    """
    Endpoint to close attendance for a specific course by its ID.
    Args:
        id (int): The ID of the course for which attendance is to be closed.
    Returns:
        JSON response indicating the result of the closure or an error message.
    Raises:
        ValueError: If there is an error closing the attendance.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    if not id:
        return jsonify({"message": "El id del curso es invalido"}), 400

    attendance_logic = AttendanceLogic()

    close_attendance = attendance_logic.close_attendance(course_id=id)

    return jsonify(close_attendance), 200


# Definicion endpoint obtencion de asistencias de un dia y un curso
@bp.route("/asistencias/revision/", methods=["POST"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def get_attendace_by_day_and_course():
    """
    Endpoint to retrieve attendances for a specific course on a specific date.
    Returns:
        JSON response with a list of attendances for the specified course and date or an error message.
    Raises:
        ValueError: If there is an error retrieving the attendances.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """
    if "course_id" not in request.json or "date_to_search" not in request.json:
        return jsonify({"message": "Missing required parameters"}), 400

    if not request.json["course_id"] or not request.json["date_to_search"]:
        return jsonify({"message": "Invalid course_id or date_to_search"}), 400

    attendance_logic = AttendanceLogic()

    attendances_response = attendance_logic.get_attendance_by_day_and_course(
        course_id=request.json["course_id"],
        date_to_search=request.json["date_to_search"],
    )

    return jsonify(attendances_response), 200


# Definicion endpoint borrado de asistencia, cambio el activo
@bp.route("/asistencias/<int:id>", methods=["DELETE"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def delete_attendance(id):
    """
    Endpoint to delete an attendance by its ID, marking it as inactive.
    Args:
        id (int): The ID of the attendance to be deleted.
    Returns:
        JSON response with the deleted attendance details or an error message.
    Raises:
        ValueError: If the attendance does not exist or there is an error retrieving it.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    attendance_logic = AttendanceLogic()

    deleted_attendance = attendance_logic.delete_attendance(id_attendance=id)

    return jsonify(deleted_attendance), 200


# Definicion endpoint creacion asistencia
@bp.route("/asistencias", methods=["POST"])
@token_required
@require_json
@handle_api_exceptions(default_message="Error retrieving attendances")
def save_attendance():
    """
    Endpoint to create a new attendance record.
    Returns:
        JSON response with the created attendance details or an error message.
    Raises:
        ValueError: If there is an error creating the attendance or if the data is invalid.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    attendance_logic = AttendanceLogic()
    new_attendance = attendance_logic.save_attendance(attendance_data=request.json)

    return jsonify(new_attendance), 201


# Definicion endpoint edicion asistencia
@bp.route("/asistencias/<int:id>", methods=["PATCH"])
@token_required
@require_json
@handle_api_exceptions(default_message="Error retrieving attendances")
def update_attendance(id):
    """
    Endpoint to update an existing attendance record by its ID.
    Args:
        id (int): The ID of the attendance to update.
    Returns:
        JSON response with the updated attendance details or an error message.
    Raises:
        ValueError: If the attendance does not exist or if the update data is invalid.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    attendance_data = request.json
    attendance_logic = AttendanceLogic()

    updated_attendance = attendance_logic.update_attendance(
        id_attendance=id, attendance_data=attendance_data
    )
    #
    return jsonify(updated_attendance), 200


# Definicion endpoint obtencion de fechas disponibles por curso
@bp.route("/asistencias/fechas/<int:course_id>", methods=["GET"])
@token_required
@handle_api_exceptions(default_message="Error retrieving attendances")
def get_available_dates_by_course(course_id):
    """
    Endpoint to retrieve available dates for attendance by course ID.
    Args:
        course_id (int): The ID of the course for which available dates are to be retrieved.
    Returns:
        JSON response with a list of available dates or an error message.
    Raises:
        ValueError: If there is an error retrieving the available dates.
        SQLAlchemyError: If there is a database error.
        Exception: For any other exceptions that occur.
    """

    attendance_logic = AttendanceLogic()

    # Convertir las fechas a formato string para la respuesta JSON
    serialized_dates = attendance_logic.get_available_dates_by_course(
        course_id=course_id
    )

    print("200 - Fechas disponibles obtenidas")
    return jsonify(serialized_dates), 200
