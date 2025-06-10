from datetime import datetime
from typing import Any, list

from src.models.models import Attendance, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, UnmappedInstanceError


class AttendanceLogic:

    def get_attendances(self) -> list[Attendance]:
        """
        Get all attendance data from the database.
        Returns:
            List of Attendance objects.
        """
        try:
            all_attendances = Attendance.query.filter(
                Attendance.active == True
                ).order_by(Attendance.id).all()

            return all_attendances
        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e

    
    def get_inactive_attendances(self) -> list[Attendance]:
        """
        Get all the inactive attendances data from the database.
        Returns:
            List of Attendance objects.
        """
        try:
            all_inactive_attendances = Attendance.query.filter(
                Attendance.active == False
                ).order_by(Attendance.id).all()

            return all_inactive_attendances
        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e


    def get_attendance_by_id(self, id:int) -> Attendance:
        """
        Get an specific attendance from the database filtered by an id.
        Args:
            id: Id of the attendance.
        Returns:
            Attendance object.
        """

        try:
            attendance = Attendance.query.filter(
                Attendance.id == id
                ).first()

            return attendance

        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e

    def get_attendances_by_student_id(self, id:int, request_data:dict[str, Any]) -> list[Attendance]:
        """
        Get the specific student's attendances filtered by it id.
        Args:
            id: Integer value with the student id.
            request_data: Dictionary with the request data.
        Returns:
            List of Attendance objects.
        """

        start_date = request_data.get('start')
        end_date = request_data.get('end')

        try:
            query = Attendance.query.filter(Attendance.student_id == id)

            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Attendance.day >= start_date)
            
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                query = query.filter(Attendance.day <= end_date)
            
            founded_attendances = query.order_by(Attendance.day.asc()).all()

            return founded_attendances

        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e

        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e


    def close_attendance(self, course_id: int) -> None:
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

        try:
            founded_course = db.session.get(Course, course_id)

            if not founded_course:
                raise ValueError(f"Course with id {course_id} not found")

            existing_attendances = Attendance.query.filter(
                db.cast(Attendance.day, db.Date) == current_date
                ).filter(
                    Attendance.course_id == course_id
                ).all()
            
            attendances_id = [attendance.student_id for attendance in existing_attendances]

            new_attendances_created = 0

            for student in founded_course.students:
                if student.id not in attendances_id:
                    new_attendance = Attendance(
                        course_id = course_id,
                        student_id = student.id,
                        state = False,
                        active = True,
                        day = current_date
                    )

                    db.session.add(new_attendance)
                    new_attendances_created += 1

            if new_attendances_created > 0:
                db.session.commit()
                print(f'200 - Asistencia cerrada para curso {course_id}. {new_attendances_created} nuevas asistencias creadas')
            else:
                print(f'200 - Asistencia para curso {course_id} ya estaba cerrada. No se crearon nuevas asistencias')
            return {'message': 'Attendance closed successfully'}

            
        except ValueError as e:
            #Captura de error si el curso no es encontrado
            db.session.rollback()
            raise ValueError(f"Validation Error: {e}") from e
        
        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
        
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e


    def get_attendance_by_day_and_course(self, course_id:int, date_to_search:str) -> list[Attendance]:
        """
        Get a list of attendances for specific course and date from the database.
        Args:
            course_id: Integer value with the course id.
            date_to_search: String value with the date to search (YYYY-MM-DD format recommended).
        Returns:
            List of Attendance objects. Returns an empty list if no attendances are found.
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
            datetime.strptime(date_to_search, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date_to_search format. Please use YYYY-MM-DD.")
        

        try:
            founded_attendances = Attendance.query.filter(
                Attendance.course_id == course_id
                ).filter(
                    db.cast(Attendance.day, db.Date) == date_to_search
                ).all()

            if founded_attendances:
                for attendance in founded_attendances:
                    attendance_dict = {}
                    temp_student = db.session.get(Student, attendance.student_id)
                    attendance_dict['names'] = temp_student.names
                    attendance_dict['surnames'] = temp_student.surnames
                    attendance_dict['state'] = attendance.state

                    attendances_response.append(attendance_dict)
            
            return attendances_response

        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e


    def delete_attendance(self, id_attendance: int) -> Attendance:
        """
        Delete an attendance from the database.
        Args:
            id_attendance: Integer value with the attendance id.
        Returns:
            Attendance object.
        """

        try:
            founded_attendance = db.session.get(Attendance, id_attendance)

            founded_attendance.active = False
            founded_attendance.updated_at = datetime.now()
            db.session.commit()

            return founded_attendance
        
        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e


    def save_attendance(self, attendance_data: dict[str, Any]) -> Attendance:
        """
        Save or toggle attendance data to the database with separate try/except blocks.
        Args:
            attendance_data: Dictionary containing attendance information.
                             For creation, includes 'student_id', 'course_id', 'state', 'active'.
                             For update, includes 'state' (and optionally others like 'active').
        Raises:
            ValueError: If required attendance_data is missing or invalid.
            IntegrityError: If a database integrity constraint is violated.
            Exception: For any other unexpected errors.
        """

        current_date = datetime.now().date()
        founded_attendance: Optional[Attendance] = None
        
        # Toggle the Attendance's 'state' field for a specifics student and day
        try:
            founded_attendance = Attendance.query.filter(
                db.cast(Attendance.day, db.Date) == current_date
                ).filter(
                Attendance.student_id == attendance_data['student_id']
                ).filter(
                Attendance.course_id == attendance_data['course_id']
                ).first()

            if founded_attendance:
                if 'state' not in attendance_data:
                    raise ValueError("Missiong 'state' field for updating attendance")
                
                founded_attendance.state = attendance_data['state']

                if 'active' in attendance_data:
                    founded_attendance.active = attendance_data['active']
                
                founded_attendance.updated_at = datetime.now()

                db.session.commit()
                return founded_attendance

        except (SQLAlchemyError, Exception) as e:
            db.session.rollback()

            if isinstance(e, SQLAlchemyError):
                raise SQLAlchemyError(f"Database error during toggle: {e}")
            else:
                raise Exception(f"An unexpected error ocurred during toggle: {e}") from e

        
        
        if not founded_attendance:
            try:

                required_data = ['student_id', 'course_id', 'state', 'active']
                for field in required_data:
                    if field not in attendance_data:
                        raise ValueError(f"Missiong required field for creation: {field}")
                new_attendance = Attendance(
                    course_id = attendance_data['course_id'],
                    student_id = attendance_data['student_id'],
                    state = attendance_data['state'],
                    active = attendance_data['active'],
                    day = current_date
                )

                db.session.add(new_attendance)
                db.session.commit()

                return new_attendance

            except ValueError as e:
                db.session.rollback()
                raise ValueError(f"Validation Error for creation: {e}") from e

            except (IntegrityError, FlushError) as e:
                db.session.rollback()
                detail = str(e.orig) if hasattr(e, 'orig') and e.orig else str(e)
                raise IntegrityError(f"Database integrity error during creation: {detail}", e.orig, e.statement, e.params) from e
            
            except (SQLAlchemyError, Exception) as e:
                db.session.rollback()
                if isinstance(e, SQLAlchemyError):
                    raise SQLAlchemyError(f"Database error during creation: {e}") from e
                else:
                    raise Exception(f"An unexpected error occurred during creation: {e}") from e
            try:
                # Confirmacion de las operaciones creadas en la sesion
                db.session.commit()
                print('201 - Asistencia creada')
                return new_attendance
            
            except Exception as e:
                print(f'400 - No se puede commit: {str(e)}')
                return {'message': 'No se puede commit'}
        
        raise Exception("Attendance save/toggle logic did not return a result.")
    
    
    def update_attendance(self, id_attendance: int, attendance_data: dict[str, Any]) -> Attendance:
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

        try:
            founded_attendance = Optional[Attendance] = db.session.get(Attendance, id_attendance)

            if not founded_attendance:
                raise ValueError(f"Attendance record with ID {id_attendance} not found.")
            
            updated = False

            if 'state' in attendance_data:
                founded_attendance.state = attendance_data['state']
                updated = True
            
            if 'day' in attendance_data:
                try:
                    founded_attendance.day = datetime.strptime(attendance_data['day'], '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError("Invalid 'day' format. Please use YYYY-MM-DD.")
                updated = True
            
            if 'active' in attendance_data:
                founded_attendance.active = attendance_data['active']
                updated = True
            
            if updated:
                founded_attendance.updated_at = datetime.now()
            
            db.session.commit()
            return founded_attendance

        except ValueError as e:
             # Capturar error si la asistencia no fue encontrada o datos de actualización inválidos
             db.session.rollback() # Rollback si se inició alguna operación antes del error de valor
             raise ValueError(f"Validation Error: {e}") from e
        
        except (SQLAlchemyError, UnmappedInstanceError) as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e


    def get_available_dates_by_course(self, course_id: int):

        try:
            unique_dates = (
                db.session.query(func.distinct(func.cast(Attendance.day, Date)))
                .filter(Attendance.course_id == course_id)
                .order_by(func.cast(Attendance.day, Date).desc())  # Orden descendente
                .all()
            )

            unique_dates = [date[0] for date in unique_dates]

            serialized_dates = [date.strftime('%Y-%m-%d') for date in unique_dates]

            return serialized_dates

        
        except SQLAlchemyError as e:
            #Captura de errores específicos de SQLAlchemy durante la consulta
            db.session.rollback()
            raise SQLAlchemyError(f"Database error while fetching attendances: {e}") from e
            
        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            db.session.rollback()
            raise Exception(f"An unexpected error occurred while fetching attendances: {e}") from e

