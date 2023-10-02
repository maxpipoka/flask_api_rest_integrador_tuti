from ..app import db



class Student(db.model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False, blank=False)
    names = db.Column(db.String(50), nullable=False, blank=False)
    surnames = db.Column(db.String(50), nullable=False, blank=False)
    address = db.Column(db.String(50), nullable=False, blank=False)
    email = db.Column(db.String(50), nullable=False, blank=False)
    tutors = db.relationship('Tutor', backref='student',lazy=True)
    createdAt = db.Column(db.DateTime(), nullable=False, blank=False)
    updatedAt = db.Column(db.DateTime(), nullable=True, blank=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'


class Tutor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False, blank=False)
    names = db.Column(db.String(50), nullable=False, blank=False)
    surnames = db.Column(db.String(50), nullable=False, blank=False)
    address = db.Column(db.String(50), nullable=False, blank=False)
    email = db.Column(db.String(50), nullable=False, blank=False)
    student_id= db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False, blank=False)
    createdAt = db.Column(db.DateTime(), nullable=False, blank=False)
    updatedAt = db.Column(db.DateTime(), nullable=True, blank=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'


class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    level = db.Column(db.Integer(), nullable=False, blank=False)
    division = db.Column(db.String(1), nullable=False, blank=False)
    year = db.Column(db.Integer, nullable=False, blank=False)
    current = db.Column(db.Boolean(), default=True, nullable=False)
    attendance = db.relationship('Attendance', backref='course', lazy=True)
    createdAt = db.Column(db.DateTime(), nullable=False, blank=False)
    updatedAt = db.Column(db.DateTime(), nullable=True, blank=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return f'{self.year} - {self.level} - {self.division}'
    

class Attendance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id'), nullable=False, blank=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False, blank=False)
    day = db.Column(db.DateTime(), nullable=False, blank=False)
    state = db.Column(db.Boolean(),  default=False, nullable=False)
    createdAt = db.Column(db.DateTime(), nullable=False, blank=False)
    updatedAt = db.Column(db.DateTime(), nullable=True, blank=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return f'{self.course_id} - {self.student_id} - {self.day}'