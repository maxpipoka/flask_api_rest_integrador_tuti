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
    # attendances = relationship('Attendance', back_populates='student')
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    course = relationship('Course', back_populates='students')

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
            'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S') if self.createdAt else None,
            'updatedAt': self.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if self.updatedAt else None,
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
    # student_id= db.Column(db.Integer(), db.ForeignKey('students.id'), nullable=True)
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
    
    def as_dict(self):

        # students_list = [student.as_dict() for student in self.students]
        return {
            'id': self.id,
            'dni': self.dni,
            'names': self.names,
            'surnames': self.surnames,
            'address': self.address,
            'email': self.email,
            # 'students': students_list,
            'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S') if self.createdAt else None,
            'updatedAt': self.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if self.updatedAt else None,
            'active': self.active
        }


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
    # attendances = relationship('Attendance', back_populates='course')
    students = relationship('Student', back_populates='course')

    def __init__(self, level, division, year, current, active):
        self.level = level
        self.division = division
        self.year = year
        self.current = current
        self.createdAt = datetime.now()
        self.active = active

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
            'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S') if self.createdAt else None,
            'updatedAt': self.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if self.updatedAt else None,
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
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, course_id, student_id, day, state, active):
        self.course_id = course_id
        self.student_id = student_id
        self.day = day
        self.state = state
        self.createdAt = datetime.now()
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
            'createdAt': self.createdAt.strftime('%d-%m-%Y') if self.createdAt else None,
            'updatedAt': self.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if self.updatedAt else None,
            'active': self.active
        }
    

