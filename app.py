from datetime import datetime
from flask import Flask, request, jsonify
import os
import psycopg2
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Carga de las variables de entorno desde el .env
load_dotenv()

# Generación instancia aplicacion de Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    tutors = db.relationship('Tutor', backref='student',lazy=True)
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
    

class Tutor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    student_id= db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
    createdAt = db.Column(db.DateTime(), nullable=False)
    updatedAt = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        self.dni = kwargs.dni
        self.names = kwargs.names
        self.surnames = kwargs.surnames
        self.address = kwargs.address
        self.email = kwargs.email
        self.student_id = kwargs.student_id
        self.createdAt = datetime.now()
        self.active = kwargs.active

    def __repr__(self):
        return f'{self.dni} - {self.surnames} {self.names}'


class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    level = db.Column(db.Integer(), nullable=False)
    division = db.Column(db.String(1), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    current = db.Column(db.Boolean(), default=True, nullable=False)
    attendance = db.relationship('Attendance', backref='course', lazy=True)
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


# Creacion de las tablas mediante el ORM en la DDBB
# with app.app_context():
#     db.create_all()

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dni', 'names', 'surnames', 'address', 'email', 'tutors', 'createdAt', 'updatedAt', 'active')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


# Guardado variable desde el entorno
# url_db = os.getenv('DB_URL')

# Creacion instancia conexion
# connection = psycopg2.connect(url_db)

# Definicion endpoint del index
@app.get('/')
def index():
    return 'Hola Mundo'

# Definicion endpoint
@app.get('/alumnos')
def getAllAlumnos():
    return 'Todos los alumnos'

# Definicion endpoint
@app.get('/alumnos/<id>')
def getOneAlumno(id):
    return 'Un solo alumno'

# Definicionn endpoint creacion alumno
@app.route('/alumnos', methods=['POST'])
def createStudent():

    print(int(request.json['dni']))
    newStudent = None

    try:
        newStudent = Student(
            dni= request.json['dni'],
            names= request.json['names'],
            surnames= request.json['surnames'],
            address= request.json['address'],
            email = request.json['email'],
            active = request.json['active']
            )
        print(newStudent)

    except KeyError as e:
        return jsonify({'message': f'Missing field: {e.args[0]}'})
    except Exception as e:
        return jsonify({'messagedd': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message':'No se puede crear la instancia'}), 400
    
    
    try:
         db.session.add(newStudent)
    except:
        return jsonify({'message':'No se puede ADD'}), 400
    
    try:
        # Confirmación de las operaciones creadas en la session
        db.session.commit()
        return jsonify({'message':'Success'}), 201
    except:
        return jsonify({'message':'No se puede commit'}), 400


if __name__ == '__main__':
    app.run(debug=True)