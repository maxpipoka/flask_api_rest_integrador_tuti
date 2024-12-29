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


class TestAttendances(TestCase):

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

        self.attendance = Attendance(
            state=True, course_id=1, student_id=self.student.id, active=True, day='2024-12-27')
        db.session.add(self.attendance)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # db.session.close()

    def get_auth_token(self):
        response = self.client.post('/auth', json={
            'username': self.user.username,
            'password': self.user.password
        })

        token = response.json.get('token')
        return token

    def test_save_attendance(self):
        token = self.get_auth_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = self.client.post('/asistencias', json={
            'state': True,
            'course_id': self.course.id,
            'student_id': self.student.id,
            'active': True
        }, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response.json['message'])

    def test_update_attendance(self):
        token = self.get_auth_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = self.client.patch(f'/asistencias/{self.attendance.id}', json={
            'state': False
        }, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['state'], False)

    def test_get_attendances(self):
        token = self.get_auth_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = self.client.get('/asistencias', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_attendance(self):
        token = self.get_auth_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = self.client.delete(f'/asistencias/{self.attendance.id}', headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
