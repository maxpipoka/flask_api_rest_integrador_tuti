import os
from flask import Flask

# Importa las extensiones que uses, pero no las inicialices aún
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# Inicializa las extensiones SIN pasarles la app
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
ma = Marshmallow()

def create_app(test_config=None):
    """Crea y configura la instancia de la aplicación Flask."""

    # Crea la instancia de Flask
    # instance_relative_config=True indica que los archivos de configuración
    # relativos se encuentran en el 'instance' folder (fuera del paquete)
    app = Flask(__name__, instance_relative_config=True)

    # Configuración de la aplicación
    if test_config is None:
        # Carga la configuración desde config.py si no está en modo test
        # Asegúrate de tener un archivo config.py en el directorio 'instance'
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carga la configuración de test si se pasa
        app.config.from_mapping(test_config)

    # Asegura que la carpeta 'instance' exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print(f"DEBUG: app.config['SQLALCHEMY_DATABASE_URI'] antes de db.init_app: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # Inicializa las extensiones con la aplicación (AHORA sí se les pasa la app)
    db.init_app(app)
    migrate.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # TODO: Registrar Blueprints aquí
    from .endpoints import students # Importación relativa correcta dentro del paquete src
    app.register_blueprint(students.bp)

    from .endpoints import tutors
    app.register_blueprint(tutors.bp)

    from .endpoints import courses
    app.register_blueprint(courses.bp)

    from .endpoints import attendances
    app.register_blueprint(attendances.bp)

    from .endpoints import users
    app.register_blueprint(users.bp)

    from .endpoints import auth
    app.register_blueprint(auth.bp)

    @app.get('/')
    def index():
        return 'Hola Mundo'

    return app
