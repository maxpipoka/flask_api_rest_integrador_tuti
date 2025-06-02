from datetime import datetime
from typing import Any

from src.models.models import Attendance, db


class AttendanceLogic:

    def save_attendance(self, attendance_data: dict[str, Any]) -> dict[str, Any]:
        """
        Save attendance data to the database.
        :param attendance_data: Dictionary containing attendance information.
        """
        # Logic to save attendance data

        current_date = datetime.now().date()
        
        # Toggle de estado de asistencia si ya exite para dia y alumno específicos
        try:
            founded_attendance = Attendance.query.filter(
                db.cast(Attendance.day, db.Date) == current_date).filter(
                Attendance.student_id == attendance_data['student_id']).filter(
                Attendance.course_id == attendance_data['course_id']).first()

            if founded_attendance:
                print('Encontrada anterior')
                print(founded_attendance.state)
                
                print('Cambiando!')
                founded_attendance.state = attendance_data['state']
                print(founded_attendance.state)

                db.session.commit()

                print('201 - Asistencia modificada')
                print(founded_attendance)

                return founded_attendance
        except Exception as e:
            print(f'Error en consulta: {str(e)}')

        
        try:
            new_attendance = Attendance(
                course_id = attendance_data['course_id'],
                student_id = attendance_data['student_id'],
                state = attendance_data['state'],
                active = attendance_data['active'],
                day = current_date
            )

        except KeyError as e:
            print('400 -' f'Missing field: {e.args[0]}')
            return {'message1': f'Missing field: {e.args[0]}'}
        
        except Exception as e:
            print('400 -' f'Error: {str(e)}')
            return {'message2': f'Error: {str(e)}'}
        
        except:
            print('400 - No se puede crear la instancia')
            return {'message3':'No se puede crear la instancia'}
        
        db.session.add(new_attendance)

        try:
            # Confirmacion de las operaciones creadas en la sesion
            db.session.commit()
            print('201 - Asistencia creada')
            return new_attendance
        
        except Exception as e:
            print(f'400 - No se puede commit: {str(e)}')
            return {'message': 'No se puede commit'}
    
    