from src.app import app, db
from flask_testing import TestCase
import sys
import os

from src.models.models import User


# Agregado del directorio 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'src')))

class TestAuth(TestCase):

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
    
    def test_get_main_page(self):
        response = self.client.get('/auth')

        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.client.post('/auth', json={
            'username': self.users[0].username,
            'password': self.users[0].password
        })

        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post('/auth/register', json={
            'username': 'cristian3',
            'password': 'passcristian3',
            'fullname': 'Cristian Krutki',
            'rol': 'Encargado de preceptores',
            'access_level': 3
        }, headers=self.headers)
        
        self.assertEqual(response.status_code, 201)