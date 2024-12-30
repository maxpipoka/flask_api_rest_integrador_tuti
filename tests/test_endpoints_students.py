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

class TestStudent(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        pass

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
    
    def test_get_students(self):
        pass

    def test_get_student_by_id(self):
        pass

    def test_delete_student(self):
        pass

    def test_save_student(self):
        pass

    def test_update_student(self):
        pass

    def test_asociate_student_to_tutor(self):
        pass
    