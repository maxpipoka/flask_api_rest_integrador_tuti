from datetime import datetime
from src.models.models import Attendance, Course, User, Student
from src.app import app, db
from flask_testing import TestCase
import sys
import os
import unittest
import uuid

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


        unique_dni = int(str(uuid.uuid4().int)[:8])  # Un entero de 8 dígitos

        # Agrega datos de prueba
        self.user = User(username='cristian', password='passcristian',
                         fullname='Cristian Krutki', rol='Preceptor', access_level=2)
        db.session.add(self.user)
        db.session.commit()

        self.course = Course(level=1, division='A', year=2024,
                             current=True, active=True, associated_user=self.user.id)
        db.session.add(self.course)
        db.session.commit()

        self.student = Student(dni=unique_dni, names='Roque Martín', surnames='Cardozo',
                               address='Calle cas de Martin', email='martincardozo@gmail.com', active=True)
        db.session.add(self.student)
        db.session.commit()

        self.attendances = []
        for i in range(5):
            boolean_value = (i % 2 == 0)
            attendance = Attendance(
            state=boolean_value, course_id=1, student_id=self.student.id, active=boolean_value, day=datetime.now().strftime('%d-%m-%Y'))
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
            'date_to_search': datetime.now().strftime('%d-%m-%Y')
        }, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)

    def test_get_attendance_by_id(self):
        request = self.client.get(f'/asistencias/{self.attendances[0].id}', headers=self.headers)

        self.assertEqual(request.status_code, 200)

    def test_delete_attendance(self):
        response = self.client.delete(
            f'/asistencias/{self.attendance.id}', headers=self.headers)
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['active'], False)

    def test_save_attendance(self):
        response = self.client.post('/asistencias', json={
            'state': True,
            'course_id': self.course.id,
            'student_id': self.student.id,
            'active': True
        }, headers=self.headers)

        self.assertEqual(response.status_code, 201)

    def test_update_attendance(self):
        response = self.client.patch(f'/asistencias/{self.attendance.id}', json={
            'state': False
        }, headers=self.headers)

        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
