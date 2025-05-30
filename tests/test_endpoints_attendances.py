from datetime import datetime
from src.models.models import Attendance, Course, User, Student
from src.app import app, db
from flask_testing import TestCase
import sys
import os
import unittest
import uuid
import time

# Agregado del directorio 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'src')))


class TestAttendance(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        # Agrega datos de prueba
        self.user = User(username='cristian', password='passcristian',
                         fullname='Cristian Krutki', rol='Preceptor', access_level=2)
        db.session.add(self.user)
        db.session.commit()

        self.course = Course(level=1, division='A', year=2024,
                             current=True, active=True, associated_user=self.user.id)
        db.session.add(self.course)

        self.course2 = Course(level=2, division='B', year=2024,
                              current=True, active=True, associated_user=self.user.id)
        db.session.add(self.course2)
        db.session.commit()

        self.students =  []

        for i in range(5):
            student = Student(dni=int(str(uuid.uuid4().int)[:8]), names='Juan Carlos', surnames='Perez',
                              address='Calle cas de Martin', email= 'juancarlos@gmail.com', active=True)
            self.students.append(student)
            db.session.add(student)
        db.session.commit()

        self.student2 = Student(dni=int(str(uuid.uuid4().int)[:8]), names='Juan Carlos', surnames='Perez',
                                address='Calle cas de Martin', email= 'juancarlos@gmail.com', active=True)
        db.session.add(self.student2)
        db.session.commit()

        self.attendances = []
        for i in range(5):
            boolean_value = (i % 2 == 0)
            attendance = Attendance(
            state=boolean_value, course_id=1, student_id=self.students[i].id, active=boolean_value, day=datetime.now().strftime('%Y-%m-%d'))
            self.attendances.append(attendance)
            db.session.add(attendance)
        db.session.commit()

        token = self.get_auth_token()

        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_auth_token(self):
        response = self.client.post('/auth', json={
            'username': self.user.username,
            'password': self.user.password
        })

        token = response.json.get('token')
        return token

    def test_get_all_attendances_with_active_field_in_true_status_code_200(self):
        response = self.client.get('/asistencias', headers=self.headers)
        self.assertEqual(response.status_code, 200)


    def test_get_all_attendances_by_student_id(self):
        response = self.client.get(f'/asistencias/alumno/{self.students[0].id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_inactive_attendances_checking_active_field_its_false(self):
        response = self.client.get('/asistencias/inactivas', 
                                             headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        print(response.json)

        for attendance in response.json:
            with self.subTest(attendance=attendance):

                self.assertEqual(attendance['active'], False)

    def test_close_attendance_by_course_and_by_day(self):
        response = self.client.post(f'/asistencias/cerrar/{self.course.id}', headers=self.headers)

        self.assertEqual(response.status_code, 200)


    def test_get_attendance_by_course_and_by_day(self):
        response = self.client.post(f'/asistencias/revision/', json={
            'course_id': self.course.id,
            'date_to_search': datetime.now().strftime('%Y-%m-%d')
        }, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)

    def test_get_attendance_by_id(self):
        request = self.client.get(f'/asistencias/{self.attendances[0].id}', headers=self.headers)

        self.assertEqual(request.status_code, 200)

    def test_delete_attendance(self):
        response = self.client.delete(
            f'/asistencias/{self.attendances[0].id}', headers=self.headers)
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['active'], False)

    def test_save_attendance(self):
        response = self.client.post('/asistencias', json={
            'state': True,
            'course_id': self.course2.id,
            'student_id': self.student2.id,
            'active': True
        }, headers=self.headers)

        self.assertEqual(response.status_code, 201)

    def test_update_attendance(self):
        response = self.client.patch(f'/asistencias/{self.attendances[0].id}', json={
            'state': False
        }, headers=self.headers)

        self.assertEqual(response.status_code, 201)

    
    def test_toggle_attendance_from_present_to_absent(self):

        today = datetime.now().date()

        initial_attendance = Attendance(
            state=True,
            course_id=self.course.id,
            student_id=self.students[0].id,
            active=True,
            day=today
        )

        db.session.add(initial_attendance)
        db.session.commit()
        initial_attendance_id = initial_attendance.id

        print(' ')
        print('Impresion db.session previa: ')
        print(db.session)
        print(' ')

        response = self.client.post('/asistencias', json={
            'state': False,
            'course_id': self.course.id,
            'student_id': self.students[0].id,
            'active': True
        }, headers=self.headers)

        # time.sleep(0.5) # Pausa para retrasar la consulta y evitar conflictos de tiempo

        print(' ')
        print('Impresion db.session post: ')
        print(db.session)
        print(' ')
        
        # Verificacion de respuesta exitosa
        self.assertEqual(response.status_code, 201)

        db.session.refresh(initial_attendance)
        db.session.commit()

        # Verificacion asistencia original este cambiada a AUSENTE
        update_attendance_after_change = db.session.query(Attendance).filter(
            Attendance.id == initial_attendance_id).filter(
                db.cast(Attendance.day, db.Date) == today).first()
        
        self.assertIsNotNone(update_attendance_after_change)
        print('Consulta post actualizacion')
        print(update_attendance_after_change)
        print(update_attendance_after_change.state)
        self.assertEqual(initial_attendance.state, False)
        
        # Verificación no se haya creado una nueva asistencia
        attendances_count = Attendance.query.filter_by(
            student_id = self.students[0].id,
            course_id = self.course.id,
            day=today
        ).count()
        self.assertEqual(attendances_count, 1)

        # Verificacion que respuesta tenga la asistencia actualizada
        self.assertEqual(response.json['state'], False)
        self.assertEqual(response.json['id'], initial_attendance_id)

    
    def test_toggle_attendance_from_absent_to_present(self):

        initial_attendance = Attendance(
            state=False,
            course_id=self.course.id,
            student_id=self.students[0].id,
            active=True,
            day=datetime.now().strftime('%Y-%m-%d')
        )

        db.session.add(initial_attendance)
        db.session.commit()

        initial_attendance_id = initial_attendance.id

        response = self.client.post('/asistencias', json={
            'state': True,
            'course_id': self.course.id,
            'student_id': self.students[0].id,
            'active': True
        }, headers=self.headers)

        # Verificacion de respuesta exitosa
        self.assertEqual(response.status_code, 201)

        # Verificacion asistencia original este cambiada a AUSENTE
        update_attendance = Attendance.query.get(initial_attendance_id)
        self.assertIsNotNone(update_attendance)
        self.assertEqual(update_attendance.state, True)

        # Verificación no se haya creado una nueva asistencia
        attendances_count = Attendance.query.filter_by(
            student_id = self.students[0].id,
            course_id = self.course.id,
            day=datetime.now().strftime('%Y-%m-%d')
        ).count()
        self.assertEqual(attendances_count, 1)

        # Verificacion que respuesta tenga la asistencia actualizada
        self.assertEqual(response.json['state'], True)
        self.assertEqual(response.json['id'], initial_attendance_id)


    def test_sqlalchemy_refresh_in_memory(self):
        # Crear y comitear una asistencia
        attendance = Attendance(
            state=True,
            course_id=self.course.id,
            student_id=self.students[0].id,
            active=True,
            day=datetime.now().strftime('%Y-%m-%d')
        )
        db.session.add(attendance)
        db.session.commit()
        attendance_id = attendance.id

        # Simular un cambio en otra "sesión" o contexto
        # Esto podría ser una nueva consulta o modificar el objeto existente y comitear
        # Opción 1: Nueva consulta (simulando otro contexto)
        other_session_attendance = db.session.query(Attendance).get(attendance_id)
        other_session_attendance.state = False
        db.session.commit() # Comitear el cambio simulado

        # Opción 2: Modificar el objeto existente y comitear (si el objeto still attached)
        # attendance.state = False
        # db.session.commit()


        # En la sesión original del test, intentar refrescar el objeto
        db.session.refresh(attendance)

        # Verificar el estado del objeto refrescado
        self.assertEqual(attendance.state, False)


if __name__ == '__main__':
    unittest.main()
