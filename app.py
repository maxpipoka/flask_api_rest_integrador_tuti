import json
from flask import Flask, Response, request, jsonify
import os
import psycopg2
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from sqlalchemy import select
from dataclasses import dataclass

from models.models import db
from models.models import Student, Tutor, Course, Attendance

# Carga de las variables de entorno desde el .env
load_dotenv()

# Generación instancia aplicacion de Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

ma = Marshmallow(app)

## Definicion de un schema que realiza la serialización del modelo para mostrado
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dni', 'names', 'surnames', 'address', 'email', 'tutors', 'createdAt', 'updatedAt', 'active')
        

# Definición de atajos de serializador
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


# Definicion endpoint del index
@app.get('/')
def index():
    return 'Hola Mundo'


# Definicion endpoint obtiene todos los alumnos
@app.route('/alumnos', methods=['GET'])
def getAllAlumnos():
    allStudents = db.session.query(Student).all()
    print(allStudents)

    serialized_students = students_schema.dump(allStudents)

    response_data = json.dumps(serialized_students, ensure_ascii=False)

    return Response(response_data, content_type='application/json; charset=utf-8'), 200

# Definicion endpoint obtiene un solo alumno filtrado por id
@app.route('/alumnos/<id>', methods=['GET'])
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
        return jsonify({'message': f'Missing field: {e.args[0]}'}), 400
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


@app.route('/alumnos/<id>', methods=['PATCH'])
def editOneAlumno(id):
    return 'Un solo alumno'


@app.route('/alumnos/<id>', methods=['DELETE'])
def removeOneAlumno(id):
    return 'Un solo alumno'

if __name__ == '__main__':
    app.run(debug=True, port=8080)