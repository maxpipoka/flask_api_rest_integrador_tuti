import sys
import os
from datetime import datetime
import uuid
from unittest import TestCase

# Importacion de la factory
from src import create_app

from bussiness_logic.attendance_logic import AttendanceLogic
from src.models.models import Attendance, Course, Student, User

# Inclusion del directorio al path para test individuales
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class TestAttendanceLogic(TestCase):

    def setUp(self):

        # Setting up the test database
        self.db_path = "test_db.sqlite"
        self.test_db_uri = f"sqlite:///{self.db_path}"

        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": self.test_db_uri,
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "SECRET_KEY": "clave_test",
            }
        )
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
                day=datetime.now(),
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
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

        # Deleting the test database file
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def get_auth_token(self):
        response = self.client.post(
            "/auth",
            json={"username": self.user.username, "password": self.user.password},
        )

        token = response.json.get("token")
        return token

    def test_save_attendance(self):

        expected = {
            "active": True,
            "course_id": self.course2.id,
            "state": True,
            "student_id": self.student2.id,
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

    def test_get_attendances(self):

        attendance_logic = AttendanceLogic()

        attendances = attendance_logic.get_attendances()

        self.assertEqual(len(attendances), len(self.attendances))
        
        ids_in_db = {a.id for a in self.attendances}
        
        ids_returned = {a["id"] if isinstance(a, dict) else a.id for a in attendances}
        
        self.assertTrue(ids_in_db.issubset(ids_returned))

    def test_get_all_attendances(self):

        

    def test_get_attendance_by_id(self):

        attendance_data = {
            "active": True,
            "course_id": self.course.id,
            "state": True,
            "student_id": self.students[0].id,
        }
        attendance_logic = AttendanceLogic()
        new_attendance = attendance_logic.save_attendance(
            attendance_data=attendance_data
        )
        attendance_id = (
            new_attendance["id"]
            if isinstance(new_attendance, dict)
            else new_attendance.id
        )

        result = attendance_logic.get_attendance_by_id(attendance_id)
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], attendance_id)

    def test_update_attendance(self):
        attendance_data = {
            "active": True,
            "course_id": self.course.id,
            "state": True,
            "student_id": self.students[1].id,
        }
        attendance_logic = AttendanceLogic()
        new_attendance = attendance_logic.save_attendance(
            attendance_data=attendance_data
        )
        attendance_id = (
            new_attendance["id"]
            if isinstance(new_attendance, dict)
            else new_attendance.id
        )

        update_data = {
            "state": False,
            "active": False,
        }
        updated_attendance = attendance_logic.update_attendance(
            attendance_id, update_data
        )
        self.assertEqual(updated_attendance.state, False)
        self.assertEqual(updated_attendance.active, False)

    def test_delete_attendance(self):
        attendance_data = {
            "active": True,
            "course_id": self.course.id,
            "state": True,
            "student_id": self.students[2].id,
        }
        attendance_logic = AttendanceLogic()
        new_attendance = attendance_logic.save_attendance(
            attendance_data=attendance_data
        )
        attendance_id = (
            new_attendance["id"]
            if isinstance(new_attendance, dict)
            else new_attendance.id
        )

        deleted_attendance = attendance_logic.delete_attendance(attendance_id)
        self.assertFalse(deleted_attendance.active)
