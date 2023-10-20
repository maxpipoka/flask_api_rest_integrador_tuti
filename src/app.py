import os

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

from sqlalchemy import select
from dataclasses import dataclass

from .models.models import db

from .endpoints.alumnos import bp as alumnos_bp


# Carga de las variables de entorno desde el .env
load_dotenv()

# Generación instancia aplicacion de Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


db.init_app(app)
ma = Marshmallow(app)

app.register_blueprint(alumnos_bp)

# Definicion endpoint del index
@app.get('/')
def index():
    return 'Hola Mundo'


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
    app.run()