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

if __name__ == '__main__':
    app.run()