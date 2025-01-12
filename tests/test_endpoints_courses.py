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

class TestCourse(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        unique_dni= int(str(uuid.uuid4().int)[:8])  # Un entero de 8 dígitos

        self.user = User(username='cristian', password='passcristian',
                         fullname='Cristian Krutki', rol='Preceptor', access_level=2)
        db.session.add(self.user)

        self.user2 = User(username='cristian2', password='passcristian2',
                          fullname='Cristian Krutki2', rol='Preceptor', access_level=2)
        db.session.add(self.user2)

        db.session.commit()

        self.courses = []

        course = Course(level=1, division='A', year=2025,
                        current=True, active=True, associated_user=self.user.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=1, division='B', year=2025,
                        current=True, active=True, associated_user=self.user.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=2, division='A', year=2025,
                        current=True, active=True, associated_user=self.user.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=2, division='B', year=2025,
                        current=True, active=True, associated_user=self.user.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=3, division='A', year=2025,
                        current=True, active=True, associated_user=self.user.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=3, division='B', year=2025,
                        current=True, active=True, associated_user=self.user.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=4, division='A', year=2025,
                        current=True, active=True, associated_user=self.user2.id)
        self.courses.append(course)
        db.session.add(course)
        course = Course(level=4, division='B', year=2025,
                        current=True, active=True, associated_user=self.user2.id)
        self.courses.append(course)
        db.session.add(course)
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
    
    def test_get_courses(self):
        response = self.client.get('/cursos', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_get_courses_by_preceptor(self):
        response = self.client.get(f'/cursos/preceptor/{self.user.id}', headers=self.headers)
        print(self.user.id)

        self.assertEqual(response.status_code, 200)

    def test_get_course_by_id(self):
        response = self.client.get(f'/cursos/{self.courses[0].id}', headers=self.headers)

    def test_delete_course(self):
        pass

    def test_asociate_student_to_course(self):
        pass

    def test_save_course(self):
        pass

    def test_update_course(self):
        pass
    