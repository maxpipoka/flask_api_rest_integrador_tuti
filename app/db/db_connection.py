import os
import psycopg2
import environ
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def get_db_connection():

    conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ['DB_USER_NAME'],
            password=os.environ['DB_PASSWORD']
            )
    
    return conn

# Open a cursor to perform database operations
cur = conn.cursor()

