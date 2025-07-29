from datetime import datetime

from sqlalchemy import func, Date

from src.utils.decorators import handle_logic_exceptions

from src.models.models import Attendance, Course, Student, db


class AttendanceLogic:

    @handle_logic_exceptions(default_message="Error al obtener las asistencias activas")
    def get_attendances(self) -> list[Attendance]:
        """
        Get all the active attendances data from the database.
        Returns:
            List of Attendance objects.
        Raises:
            ValueError: If no active attendances are found.
            SQLAlchemyError: If a database error occurs during the query.
            Exception: For any other unexpected errors.
        """

        all_attendances = (
            Attendance.query.filter(Attendance.active == True)
            .order_by(Attendance.id)
            .all()
        )

        if not all_attendances:
            raise ValueError(f"No active attendances found in the database.")

        serialized_attendances = [
            attendance.as_dict() for attendance in all_attendances
        ]

        return serialized_attendances

    @handle_logic_exceptions(
        default_message="Error al obtener las asistencias inactivas"
    )
    def get_inactive_attendances(self) -> list[Attendance]:
        """
        Get all the inactive attendances data from the database.
        Returns:
            List of Attendance objects.
        Raises:
            ValueError: If no inactive attendances are found.
            SQLAlchemyError: If a database error occurs during the query.
            Exception: For any other unexpected errors.
        """

        all_inactive_attendances = (
            Attendance.query.filter(Attendance.active == False)
            .order_by(Attendance.id)
            .all()
        )

        if not all_inactive_attendances:
            raise ValueError(f"No inactive attendances found in the database.")

        serialized_inactive_attendances = [
            attendance.as_dict() for attendance in all_inactive_attendances
        ]

        return serialized_inactive_attendances

    @handle_logic_exceptions(default_message="Error al obtener los tutores activos")
    def get_attendance_by_id(self, id: int) -> Attendance:
        """
        Get a specific attendance by its id from the database.
        Args:
            id: Integer value with the attendance id.
        Returns:
            Attendance object.
        Raises:
            ValueError: If the attendance with the given id is not found.
            SQLAlchemyError: If a database error occurs during the query.
            Exception: For any other unexpected errors.
        """

        attendance = Attendance.query.filter(Attendance.id == id).first()

        if not attendance:
            raise ValueError(f"Attendance with id {id} not found in the database.")

        return attendance

    @handle_logic_exceptions(default_message="Error al obtener los tutores activos")
    def get_attendances_by_student_id(
        self, id: int, request_data: dict[str, Any]
    ) -> list[Attendance]:
        """
        Get a list of attendances for a specific student by their id from the database.
        Args:
            id: Integer value with the student id.
            request_data: Dictionary containing 'start' and 'end' date strings in YYYY-MM-DD format.
        Returns:
            List of Attendance objects. Returns an empty list if no attendances are found.
        Raises:
            ValueError: If required input data is missing or invalid.
            SQLAlchemyError: If a database error occurs during the query.
            Exception: For any other unexpected errors.
        """

        start_date = request_data.get("start")
        end_date = request_data.get("end")

        query = Attendance.query.filter(Attendance.student_id == id)

        if not query:
            raise ValueError(f"No attendances found for student with id {id}.")

        if not start_date:
            raise ValueError("Missing required input: start_date")

        if not end_date:
            raise ValueError("Missing required input: end_date")

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Attendance.day >= start_date)

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Attendance.day <= end_date)

        ordered_attendances = query.order_by(Attendance.day.asc()).all()

        serialized_attendances = [
            attendance.as_dict() for attendance in ordered_attendances
        ]

        return serialized_attendances

    @handle_logic_exceptions(default_message="Error al cerrar la asistencia")
    def close_attendance(self, course_id: int) -> dict[str, str]:
        """
        Close the attendance for a specific course.
        Args:
            course_id: Integer value with the course id.
        Returns:
            A dictionary indicating the success of the operation.
        Raises:
            ValueError: If the course is not found.
            SQLAlchemyError: If a database error occurs during the operation.
            Exception: For any other unexpected errors.
        """

        current_date = datetime.now().date()
        attendances_id = []

        founded_course = db.session.get(Course, course_id)

        if not founded_course:
            raise ValueError(f"Course with id {course_id} not found")

        existing_attendances = (
            Attendance.query.filter(db.cast(Attendance.day, db.Date) == current_date)
            .filter(Attendance.course_id == course_id)
            .all()
        )

        attendances_id = [attendance.student_id for attendance in existing_attendances]

        new_attendances_created = 0

        for student in founded_course.students:
            if student.id not in attendances_id:
                new_attendance = Attendance(
                    course_id=course_id,
                    student_id=student.id,
                    state=False,
                    active=True,
                    day=current_date,
                )

                db.session.add(new_attendance)
                new_attendances_created += 1

        if new_attendances_created > 0:
            db.session.commit()
            print(
                f"200 - Asistencia cerrada para curso {course_id}. {new_attendances_created} nuevas asistencias creadas"
            )
        else:
            print(
                f"200 - Asistencia para curso {course_id} ya estaba cerrada. No se crearon nuevas asistencias"
            )
        return {"message": "Attendance closed successfully"}

    @handle_logic_exceptions(default_message="Error al obtener los tutores activos")
    def get_attendance_by_day_and_course(
        self, course_id: int, date_to_search: str
    ) -> list[Attendance]:
        """
        Get attendances for a specific course on a specific date.
        Args:
            course_id: Integer value with the course id.
            date_to_search: String value with the date to search in YYYY-MM-DD format.
        Returns:
            List of dictionaries containing student names, surnames, and attendance state.
        Raises:
            ValueError: If required input data is missing or invalid.
            SQLAlchemyError: If a database error occurs during the query.
            Exception: For any other unexpected errors.
        """

        if not course_id:
            raise ValueError("Missing required input: course_id")

        if not date_to_search:
            raise ValueError("Missing required input: date_to_search")

        try:
            datetime.strptime(date_to_search, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date_to_search format. Please use YYYY-MM-DD.")

        attendances_response = []

        founded_attendances = (
            Attendance.query.filter(Attendance.course_id == course_id)
            .filter(db.cast(Attendance.day, db.Date) == date_to_search)
            .all()
        )

        if not founded_attendances:
            raise ValueError(
                f"No attendances found for course {course_id} on date {date_to_search}."
            )

        if founded_attendances:
            for attendance in founded_attendances:
                attendance_dict = {}
                temp_student = db.session.get(Student, attendance.student_id)
                attendance_dict["names"] = temp_student.names
                attendance_dict["surnames"] = temp_student.surnames
                attendance_dict["state"] = attendance.state

                attendances_response.append(attendance_dict)

        return attendances_response

    @handle_logic_exceptions(default_message="Error al eliminar la asistencia")
    def delete_attendance(self, id_attendance: int) -> Attendance:
        """
        Delete an attendance from the database.
        Args:
            id_attendance: Integer value with the attendance id.
        Returns:
            Attendance object.
        """

        founded_attendance = db.session.get(Attendance, id_attendance)

        if not founded_attendance:
            raise ValueError(f"Attendance record with ID {id_attendance} not found.")

        founded_attendance.active = False
        founded_attendance.updated_at = datetime.now()
        db.session.commit()

        return founded_attendance

    @handle_logic_exceptions(default_message="Error al guardar la asistencia")
    def save_attendance(self, attendance_data: dict[str, Any]) -> Attendance:
        """
        Save or toggle attendance data to the database.
        Args:
            attendance_data: Dictionary containing attendance information.
                            For creation, includes 'student_id', 'course_id', 'state', 'active'.
                            For update, includes 'state' (and optionally others like 'active').
        Returns:
            Attendance: The saved or updated attendance record.
        Raises:
            ValueError: If required attendance_data is missing or invalid.
            IntegrityError: If a database integrity constraint is violated.
            Exception: For any other unexpected errors.
        """

        current_date = datetime.now().date()

        # Try to find existing attendance for today
        founded_attendance = (
            Attendance.query.filter(db.cast(Attendance.day, db.Date) == current_date)
            .filter(Attendance.student_id == attendance_data["student_id"])
            .filter(Attendance.course_id == attendance_data["course_id"])
            .first()
        )

        # If attendance exists, update it
        if founded_attendance:
            if "state" not in attendance_data:
                raise ValueError("Missing 'state' field for updating attendance")

            founded_attendance.state = attendance_data["state"]

            if "active" in attendance_data:
                founded_attendance.active = attendance_data["active"]

            founded_attendance.updated_at = datetime.now()
            db.session.commit()
            return founded_attendance

        # If no attendance exists, create new one
        required_data = ["student_id", "course_id", "state", "active"]
        missing = [field for field in required_data if field not in attendance_data]
        if missing:
            raise ValueError(
                f"Missing required fields for creation: {', '.join(missing)}"
            )

        new_attendance = Attendance(
            course_id=attendance_data["course_id"],
            student_id=attendance_data["student_id"],
            state=attendance_data["state"],
            active=attendance_data["active"],
            day=current_date,
        )

        db.session.add(new_attendance)
        db.session.commit()
        return new_attendance

    @handle_logic_exceptions(default_message="Error al actualizar la asistencia.")
    def update_attendance(
        self, id_attendance: int, attendance_data: dict[str, Any]
    ) -> Attendance:
        """
        Update attendance data for a specific attendance record.
        Args:
            id_attendance: The ID of the attendance record to update.
            attendance_data: Dictionary containing updated attendance information (e.g., 'state', 'day', 'active').
        Returns:
            The updated Attendance object.
        Raises:
            ValueError: If the attendance record with the given ID is not found, or if update data is invalid.
            SQLAlchemyError: If a database error occurs during the update.
            Exception: For any other unexpected errors.
        """

        founded_attendance = db.session.get(Attendance, id_attendance)

        if not founded_attendance:
            raise ValueError(f"Attendance record with ID {id_attendance} not found.")

        updated = False

        if "state" in attendance_data:
            founded_attendance.state = attendance_data["state"]
            updated = True

        if "day" in attendance_data:
            try:
                founded_attendance.day = datetime.strptime(
                    attendance_data["day"], "%Y-%m-%d"
                ).date()
            except ValueError:
                raise ValueError("Invalid 'day' format. Please use YYYY-MM-DD.")
            updated = True

        if "active" in attendance_data:
            founded_attendance.active = attendance_data["active"]
            updated = True

        if updated:
            founded_attendance.updated_at = datetime.now()

        db.session.commit()
        return founded_attendance

    @handle_logic_exceptions(default_message="Error al obtener las fechas disponibles.")
    def get_available_dates_by_course(self, course_id: int):
        """
        Get all unique attendance dates for a specific course.
        Args:
            course_id: Integer value with the course id.
        Returns:
            List of unique dates in YYYY-MM-DD format.
        Raises:
            ValueError: If no attendance dates are found for the course.
            SQLAlchemyError: If a database error occurs during the query.
            Exception: For any other unexpected errors.
        """

        unique_dates = (
            db.session.query(func.distinct(func.cast(Attendance.day, Date)))
            .filter(Attendance.course_id == course_id)
            .order_by(func.cast(Attendance.day, Date).desc())  # Orden descendente
            .all()
        )

        if not unique_dates:
            raise ValueError(
                f"No attendance dates found for course with ID {course_id}."
            )

        unique_dates = [date[0] for date in unique_dates]

        serialized_dates = [date.strftime("%Y-%m-%d") for date in unique_dates]

        return serialized_dates
