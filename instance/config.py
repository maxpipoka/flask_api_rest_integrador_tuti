# Carga las variables de entorno para usarlas aquí
import os
from dotenv import load_dotenv
load_dotenv() # Asegúrate de que .env se carga aquí si es necesario

# Configuración general de la aplicación
SECRET_KEY = os.getenv('SECRET_KEY', 'una_clave_super_secreta_por_defecto') # ¡CAMBIA ESTO en tu .env!
# Puedes añadir otras configuraciones generales aquí si las necesitas

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'sqlite:///proyecto.db') # Usa tu variable de entorno o un valor por defecto
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() in ('true', '1') # Configurable desde .env

# Configuración de JWT
JWT_SECRET_KEY = os.getenv('SECRET_JWT_KEY', 'otra_clave_secreta_para_jwt') # ¡CAMBIA ESTO en tu .env!
# Puedes añadir otras configuraciones de JWT aquí si las necesitas

# Configuración de CORS
# Permitir todas las orígenes (temporalmente para pruebas)
CORS_ORIGINS = "*"
# O permitir solo dominios específicos (descomenta y configura en .env)
# CORS_ORIGINS = os.getenv('FRONTEND_URL', '*') # Si quieres controlar desde .env
# CORS_SUPPORTS_CREDENTIALS = True # Si tu frontend necesita enviar cookies/auth headers

# Puedes añadir aquí cualquier otra configuración específica de la instancia o entorno
# Por ejemplo, detalles de un servicio externo, claves API, etc.