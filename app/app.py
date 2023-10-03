from flask import Flask
import os
import psycopg2
from dotenv import load_dotenv

# Carga de las variables de entorno desde el .env
load_dotenv()

# Generación instancia aplicacion de Flask
app = Flask(__name__)

# Guardado variable desde el entorno
url_db = os.getenv('DB_URL')

# Creacion instancia conexion
connection = psycopg2.connect(url_db)

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


if __name__ == '__main__':
    app.run(debug=True)