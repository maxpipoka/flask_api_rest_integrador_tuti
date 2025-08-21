import sys
import os
from datetime import datetime
import uuid
from unittest import TestCase

# Importacion de la factory
from src import create_app

from bussiness_logic.attendance_logic import AttendanceLogic
from src.models.models import Attendance, Course, Student, User

#Inclusion del directorio al path para test individuales
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class TestAttendanceLogic(TestCase):

    def setUp(self):

        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory',
            'SECRET_KEY': 'clave_test'
        })
        self.app_context = self.app.app_context()
        self.app_context.push()

        from src import db
        self.db = db

        self.client = self.app.test_client()

        db.create_all()

        # Agrega datos de prueba
        self.user = User(
            username="cristian",
            password="passcristian",
            fullname="Cristian Krutki",
            rol="Preceptor",
            access_level=2,
        )
        db.session.add(self.user)
        db.session.commit()

        self.course = Course(
            level=1,
            division="A",
            year=2024,
            current=True,
            active=True,
            associated_user=self.user.id,
        )
        db.session.add(self.course)

        self.course2 = Course(
            level=2,
            division="B",
            year=2024,
            current=True,
            active=True,
            associated_user=self.user.id,
        )
        db.session.add(self.course2)
        db.session.commit()

        self.students = []

        for i in range(5):
            student = Student(
                dni=int(str(uuid.uuid4().int)[:8]),
                names="Juan Carlos",
                surnames="Perez",
                address="Calle cas de Martin",
                email="juancarlos@gmail.com",
                active=True,
            )
            self.students.append(student)
            db.session.add(student)
        db.session.commit()

        self.student2 = Student(
            dni=int(str(uuid.uuid4().int)[:8]),
            names="Juan Carlos",
            surnames="Perez",
            address="Calle cas de Martin",
            email="juancarlos@gmail.com",
            active=True,
        )
        db.session.add(self.student2)
        db.session.commit()

        self.attendances = []
        for i in range(5):
            boolean_value = i % 2 == 0
            attendance = Attendance(
                state=boolean_value,
                course_id=1,
                student_id=self.students[i].id,
                active=boolean_value,
                day=datetime.now().strftime("%Y-%m-%d"),
            )
            self.attendances.append(attendance)
            db.session.add(attendance)
        db.session.commit()

        token = self.get_auth_token()

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_auth_token(self):
        response = self.client.post(
            "/auth",
            json={"username": self.user.username, "password": self.user.password},
        )

        token = response.json.get("token")
        return token

    def test_save_attendance(self):
        # Example test case for attendance logic

        expected = {
            "active": True, 
            "course_id": self.course2.id, 
            "state": True, 
            "student_id": self.student2.id
        }

        attendance_data = {
            "active": True,
            "course_id": self.course2.id,
            "state": True,
            "student_id": self.student2.id,
        }

        attendance = AttendanceLogic()

        actual = attendance.save_attendance(attendance_data=attendance_data)
        
        keys = ["active", "course_id", "state", "student_id"]
        
        actual_filtered = {k: actual[k] for k in keys}

        self.assertEqual(expected, actual_filtered)  # Replace with actual test logic
