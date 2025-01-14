from src.models.models import Attendance, Course, Tutor, User, Student
from src.app import app, db
from flask_testing import TestCase
import sys
import os
import unittest
import uuid

# Agregado del directorio 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'src')))

class TestTutor(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        self.users = []

        user = User(username='cristian', password='passcristian',
                         fullname='Cristian Krutki', rol='Preceptor', access_level=2)
        db.session.add(user)
        self.users.append(user)

        user = User(username='cristian2', password='passcristian2',
                          fullname='Cristian Krutki2', rol='Preceptor', access_level=2)
        
        db.session.add(user)
        self.users.append(user)

        db.session.commit()

        self.students = []

        for i in range(10):
            student = Student(dni=int(str(uuid.uuid4().int)[:8]), names='Juan', surnames='Perez', 
                              address='Calle falsa 123', email= f'studentjuan{i}@gmail.com', active=True)
            self.students.append(student)
            db.session.add(student)
        db.session.commit()

        self.tutors = []

        for i in range(10):
            tutor = Tutor(dni=int(str(uuid.uuid4().int)[:8]), names='Juan', surnames='Perez', 
                              address='Calle falsa 123', email=f'tutorjuan{i}@gmail.com', active=True)
            self.tutors.append(tutor)
            db.session.add(tutor)
        db.session.commit()

        token = self.get_auth_token()

        self.headers= {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_auth_token(self):
        response = self.client.post('/auth', json={
            'username': self.users[0].username,
            'password': self.users[0].password
        })

        token = response.json.get('token')
        return token
    
    def test_get_tutors(self):
        response = self.client.get('/tutores', headers= self.headers)

        self.assertEqual(response.status_code, 200)

    def test_get_tutor_by_id(self):
        response = self.client.get(f'/tutores/{self.tutors[0].id}', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_tutor(self):
        response = self.client.delete(f'/tutores/{self.tutors[0].id}', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_save_tutor(self):
        response = self.client.post('/tutores', json={
            'dni': int(str(uuid.uuid4().int)[:8]),
            'names': 'Juan',
            'surnames': 'Perez',
            'address': 'Calle falsa 123',
            'email': 'juanperez@gmail.com',
            'active': True,
            }, headers=self.headers)
        
        self.assertEqual(response.status_code, 201)

    def test_update_tutor(self):
        response = self.client.patch(f'/tutores/{self.tutors[0].id}', json={
            'names': 'Juan Carlos',
            'surname': 'Perez Companc',
            }, headers=self.headers)
        
        self.assertEqual(response.status_code, 201)

