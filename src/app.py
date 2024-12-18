import os

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv

from sqlalchemy import select
from dataclasses import dataclass

from .models.models import db

from .endpoints.students import bp as alumnos_bp
from .endpoints.tutors import bp as tutores_bp
from .endpoints.courses import bp as courses_bp
from .endpoints.attendances import bp as attendances_bp
from .endpoints.auth import bp as auth_bp


# Carga de las variables de entorno desde el .env
load_dotenv()

# Generación instancia aplicacion de Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO'] = True


db.init_app(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

app.register_blueprint(alumnos_bp)
app.register_blueprint(tutores_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(attendances_bp)
app.register_blueprint(auth_bp)

# Definicion endpoint del index
@app.get('/')
def index():
    return 'Hola Mundo'

if __name__ == '__main__':
    app.run()