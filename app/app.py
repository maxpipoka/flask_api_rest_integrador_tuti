from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from db import get_db_connection
from models import Student



app = Flask(__name__)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Hola Mundo'

@app.route('/alumnos')
def getAllAlumnos():
    pass

@app.route('/alumnos/<id>')
def getOneAlumno(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)