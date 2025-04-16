from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Tabla intermedia para la relación muchos a muchos
students_tutors = db.Table(
    'students_tutors',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.id'))
)

# Tabla intermedia para la relación muchos a muchos
students_courses = db.Table(
    'students_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

@dataclass
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    tutors = relationship('Tutor', secondary=students_tutors, back_populates='students')
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    course = relationship('Course', secondary=students_courses, back_populates='students')

    def __init__(self, dni, names, surnames, address, email, active=True):
        self.dni = dni
        self.names = names
        self.surnames = surnames
        self.address = address
        self.email = email
        self.created_at = datetime.now()
        self.active = active

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'
    
    #Funcion para serializar un alumno
    def as_dict(self):

        tutors_list = [tutor.as_dict() for tutor in self.tutors]

        return {
            'id': self.id,
            'dni': self.dni,
            'names': self.names,
            'surnames': self.surnames,
            'address': self.address,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'active': self.active,
            'tutors': tutors_list
        }
    
@dataclass    
class Tutor(db.Model):
    __tablename__ = 'tutors'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    students = relationship('Student', secondary=students_tutors, back_populates='tutors')
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, dni, names, surnames, address, email, active=True):
        self.dni = dni
        self.names = names
        self.surnames = surnames
        self.address = address
        self.email = email
        self.created_at = datetime.now()
        self.active = active

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'
    
    def as_dict(self, include_students=True):

        students_list = [student.as_dict(include_tutors=False) for student in self.students] if include_students else []
        
        return {
            'id': self.id,
            'dni': self.dni,
            'names': self.names,
            'surnames': self.surnames,
            'address': self.address,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'active': self.active,
            'students': students_list
        }


class Course(db.Model):
    __tablename__ = 'courses'    

    id = db.Column(db.Integer(), primary_key=True)
    level = db.Column(db.Integer(), nullable=False)
    division = db.Column(db.String(1), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    current = db.Column(db.Boolean(), default=True, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    students = relationship('Student', secondary=students_courses, back_populates='course')
    associated_user = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, level, division, year, current, associated_user, active=True):
        self.level = level
        self.division = division
        self.year = year
        self.current = current
        self.created_at = datetime.now()
        self.active = active
        self.associated_user = associated_user

    def __repr__(self):
        return f'{self.year} - {self.level} - {self.division}'
    
    #Funcion para serializar un curso
    def as_dict(self):

        students_list = [student.as_dict() for student in self.students]

        return {
            'id': self.id,
            'level': self.level,
            'division': self.division,
            'year': self.year,
            'current': self.current,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'active': self.active,
            'students': students_list
        }
    

class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'), nullable=False)
    day = db.Column(db.DateTime(), nullable=False)
    state = db.Column(db.Boolean(),  default=False, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, course_id, student_id, day, state, active=True):
        self.course_id = course_id
        self.student_id = student_id
        self.day = day
        self.state = state
        self.created_at = datetime.now()
        self.active = active

    def __repr__(self):
        return f'{self.course_id} - {self.student_id} - {self.day}'
    

    #Funcion para serielizar una asistencia
    def as_dict(self):
        
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'day': self.day.strftime('%d-%m-%Y'),
            'state': self.state,
            'created_at': self.created_at.strftime('%d-%m-%Y') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'active': self.active
        }
    

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    access_level = db.Column(db.Integer(), nullable=False)

    def __init__(self, username, password, fullname, rol, access_level):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.rol = rol
        self.access_level = access_level
        self.created_at = datetime.now()

    
    def __repr__(self):
        return f'{self.username} - {self.fullname}'
    
    def as_dict(self):
        
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'rol': self.rol,
            'access_level': self.access_level,
            'active': self.active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }    

