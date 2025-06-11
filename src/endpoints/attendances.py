from flask import Blueprint, request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from bussiness_logic.attendance_logic import AttendanceLogic

from src.utils.decorators import token_required, require_json

bp = Blueprint("asistencias", __name__)


# Definicion endpoint obtiene las asistencias
@bp.route("/asistencias", methods=["GET"])
@token_required
def get_attendances():

    attendance_logic = AttendanceLogic()

    active_attendances = attendance_logic.get_attendances()

    serialized_attendances = [attendance.as_dict() for attendance in active_attendances]

    return jsonify(serialized_attendances), 200


# Definicion endpoint obtiene las asistencias inactivas
@bp.route("/asistencias/inactivas", methods=["GET"])
@token_required
def get_inactive_attendances():

    attendance_logic = AttendanceLogic()

    inactive_attendances = attendance_logic.get_inactive_attendances()

    serialized_attendances = [
        attendance.as_dict() for attendance in inactive_attendances
    ]

    return jsonify(serialized_attendances), 200


# Definicion endpoint obtencion una asistencia por id
@bp.route("/asistencias/<int:id>", methods=["GET"])
@token_required
def get_attendance_by_id(id):

    attendance_logic = AttendanceLogic()

    founded_attendance = attendance_logic.get_attendance_by_id(id)

    return jsonify(founded_attendance), 200


# Definicion endpoint obtencion de asistencias por id de alumno
@bp.route("/asistencias/alumno/<int:id>", methods=["GET"])
@token_required
def get_attendances_by_student_id(id):

    if "start" not in request.args or "end" not in request.args:
        return jsonify({"message": "Missing required date filters"}), 400

    attendance_logic = AttendanceLogic()

    founded_attendances = attendance_logic.get_attendances_by_student_id(
        id, request_data=request.args
    )

    serialized_attendances = [
        attendance.as_dict() for attendance in founded_attendances
    ]

    return jsonify(serialized_attendances), 200


# Definicion endpoint para cerra asistencia de un curso en un dia
@bp.route("/asistencias/cerrar/<int:id>", methods=["POST"])
@token_required
def close_attendance(id):

    attendance_logic = AttendanceLogic()

    close_attendance = attendance_logic.close_attendance(course_id=id)

    return jsonify(close_attendance), 200


# Definicion endpoint obtencion de asistencias de un dia y un curso
@bp.route("/asistencias/revision/", methods=["POST"])
@token_required
def get_attendace_by_day_and_course():

    attendance_logic = AttendanceLogic()

    attendances_response = attendance_logic.get_attendance_by_day_and_course(
        course_id=request.json["course_id"],
        date_to_search=request.json["date_to_search"],
    )

    return jsonify(attendances_response), 200


# Definicion endpoint borrado de asistencia, cambio el activo
@bp.route("/asistencias/<int:id>", methods=["DELETE"])
@token_required
def delete_attendance(id):

    attendance_logic = AttendanceLogic()

    deleted_attendance = attendance_logic.delete_attendance(id_attendance=id)

    return jsonify(deleted_attendance), 200


# Definicion endpoint creacion asistencia
@bp.route("/asistencias", methods=["POST"])
@token_required
@require_json
def save_attendance():

    try:
        attendance_logic = AttendanceLogic()
        new_attendance = attendance_logic.save_attendance(attendance_data=request.json)

        return jsonify(new_attendance), 201

    except ValueError as e:
        # Manejar error si la asistencia no fue encontrada o datos de actualización inválidos
        print(f"Validation or Not Found Error: {e}")  # Loggear el error
        # Si el mensaje de error de la lógica indica que no se encontró, devuelve 404
        return jsonify({"message": str(e)}), 400  # Bad Request

    except SQLAlchemyError as e:
        # Manejar errores de base de datos
        print(f"Database Error: {e}")  # Loggear el error
        return (
            jsonify({"message": "Database error: Could not update attendance."}),
            500,
        )  # Internal Server Error

    except Exception as e:
        # Manejar otros errores inesperados
        print(f"Internal Server Error: {e}")  # Loggear el error interno
        return jsonify({"message": "An internal server error occurred."}), 500


# Definicion endpoint edicion asistencia
@bp.route("/asistencias/<int:id>", methods=["PATCH"])
@token_required
@require_json
def update_attendance(id):

    try:
        attendance_data = request.json
        attendance_logic = AttendanceLogic()

        updated_attendance = attendance_logic.update_attendance(
            id_attendance=id, attendance_data=attendance_data
        )

        return jsonify(updated_attendance), 200

    except ValueError as e:
        # Manejar error si la asistencia no fue encontrada o datos de actualización inválidos
        print(f"Validation or Not Found Error: {e}")  # Loggear el error
        # Si el mensaje de error de la lógica indica que no se encontró, devuelve 404
        if f"Attendance record with ID {id} not found" in str(e):
            return jsonify({"message": str(e)}), 404  # Not Found
        else:
            # Para otros errores de validación, devuelve 400
            return jsonify({"message": str(e)}), 400  # Bad Request

    except SQLAlchemyError as e:
        # Manejar errores de base de datos
        print(f"Database Error: {e}")  # Loggear el error
        return (
            jsonify({"message": "Database error: Could not update attendance."}),
            500,
        )  # Internal Server Error

    except Exception as e:
        # Manejar otros errores inesperados
        print(f"Internal Server Error: {e}")  # Loggear el error interno
        return jsonify({"message": "An internal server error occurred."}), 500


# Definicion endpoint obtencion de fechas disponibles por curso
@bp.route("/asistencias/fechas/<int:course_id>", methods=["GET"])
@token_required
def get_available_dates_by_course(course_id):
    try:
        attendance_logic = AttendanceLogic()

        # Convertir las fechas a formato string para la respuesta JSON
        serialized_dates = attendance_logic.get_available_dates_by_course(
            course_id=course_id
        )

        print("200 - Fechas disponibles obtenidas")
        return jsonify(serialized_dates), 200

    except Exception as e:
        print(f"500 - Error al obtener las fechas disponibles: {str(e)}")
        return jsonify({"message": "Error al obtener las fechas disponibles"}), 500
