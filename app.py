# app.py (en la RAÍZ del proyecto)

from .src import create_app

app = create_app()

# Este bloque es solo para ejecutar la app con el servidor de desarrollo de Flask
# En producción, un servidor WSGI (como Gunicorn o uWSGI) llamaría a la variable 'app'
if __name__ == '__main__':
    app.run(debug=True) # O con la configuración que necesites