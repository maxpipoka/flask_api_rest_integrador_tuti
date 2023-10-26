from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import relationship

db = SQLAlchemy()

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
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, dni, names, surnames, address, email, active):
        self.dni = dni
        self.names = names
        self.surnames = surnames
        self.address = address
        self.email = email
        self.createdAt = datetime.now()
        self.active = active

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'
    
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
    student_id= db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=True)
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, dni, names, surnames, address, email, student_id, active):
        self.dni = dni
        self.names = names
        self.surnames = surnames
        self.address = address
        self.email = email
        self.createdAt = datetime.now()
        self.student_id = student_id
        self.active = active

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer(), primary_key=True)
    level = db.Column(db.Integer(), nullable=False)
    division = db.Column(db.String(1), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    current = db.Column(db.Boolean(), default=True, nullable=False)
    # attendance = db.relationship('Attendance', backref='course', lazy=True)
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        self.level = kwargs.level
        self.division = kwargs.division
        self.year = kwargs.year
        self.current = kwargs.current
        self.createdAt = datetime.now()
        self.active = kwargs.active

    def __repr__(self):
        return f'{self.year} - {self.level} - {self.division}'
    

class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
    day = db.Column(db.DateTime(), nullable=False)
    state = db.Column(db.Boolean(),  default=False, nullable=False)
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        self.course_id = kwargs.course_id
        self.student_id = kwargs.student_id
        self.day = kwargs.day
        self.state = kwargs.state
        self.createdAt = datetime.now()
        self.active = kwargs.active

    def __repr__(self):
        return f'{self.course_id} - {self.student_id} - {self.day}'
    

# Tabla intermedia para la relación muchos a muchos
students_tutors = db.Table(
    'students_tutors',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.id'))
)