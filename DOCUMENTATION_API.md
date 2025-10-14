
# Documentación de la API

## Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:

- **`src/`**: Contiene el código fuente principal de la aplicación.
    - **`endpoints/`**: Define los endpoints de la API, cada archivo corresponde a una entidad del sistema.
    - **`models/`**: Contiene los modelos de la base de datos y los esquemas de serialización.
        - **`models.py`**: Define las clases que mapean a las tablas de la base de datos utilizando SQLAlchemy. Cada clase representa una tabla y sus atributos son las columnas de la tabla.
        - **`schemas.py`**: Define los esquemas de Marshmallow que se utilizan para serializar y deserializar los objetos de SQLAlchemy a y desde formato JSON.
    - **`utils/`**: Contiene utilidades y decoradores reutilizables.
        - **`decorators.py`**: Contiene decoradores de Python que se utilizan para añadir funcionalidades a los endpoints, como la verificación de tokens de autenticación (`token_required`), la validación de que el `Content-Type` de la petición sea `application/json` (`require_json`) y el manejo de excepciones (`handle_api_exceptions` y `handle_logic_exceptions`).
        - **`security.py`**: Contiene las funciones para generar (`generate_token`) y decodificar (`decode_token`) los JSON Web Tokens (JWT) que se utilizan para la autenticación en la API.

- **`bussiness_logic/`**: Contiene la lógica de negocio de la aplicación, separada de la capa de presentación. Cada archivo se corresponde con una entidad del sistema y encapsula las reglas de negocio y las interacciones con la base de datos para esa entidad.
    - **`attendance_logic.py`**: Lógica de negocio para la gestión de asistencias.
    - **`auth_logic.py`**: Lógica de negocio para la autenticación y registro de usuarios.
    - **`course_logic.py`**: Lógica de negocio para la gestión de cursos.
    - **`student_logic.py`**: Lógica de negocio para la gestión de alumnos.
    - **`tutor_logic.py`**: Lógica de negocio para la gestión de tutores.
    - **`user_logic.py`**: Lógica de negocio para la gestión de usuarios.

- **`migrations/`**: Contiene las migraciones de la base de datos generadas con Alembic. Las migraciones son scripts que permiten versionar y aplicar cambios en la estructura de la base de datos de forma controlada y sistemática.

- **`tests/`**: Contiene las pruebas de la aplicación. Las pruebas son fundamentales para asegurar la calidad y el correcto funcionamiento del código.
    - **Funcionamiento**: Las pruebas utilizan el framework `unittest` y la extensión `flask-testing`. Se configuran para usar una base de datos SQLite en memoria, lo que garantiza que las pruebas se ejecuten en un entorno aislado y no afecten la base de datos de desarrollo.
    - **Estructura de una prueba**:
        - **`setUp`**: Este método se ejecuta antes de cada prueba. Se encarga de crear la estructura de la base de datos (`db.create_all()`) y de insertar los datos necesarios para la prueba (usuarios, cursos, alumnos, etc.). Para las pruebas de endpoints que requieren autenticación, también se simula un inicio de sesión para obtener un token de autorización.
        - **`tearDown`**: Este método se ejecuta después de cada prueba. Su función es limpiar la base de datos (`db.drop_all()`), asegurando que cada prueba comience con un estado limpio y no interfiera con las demás.
        - **Métodos `test_*`**: Cada método cuyo nombre comienza con `test_` es una prueba individual. Utilizan un cliente de prueba (`self.client`) para simular peticiones HTTP a los diferentes endpoints. Dentro de cada prueba, se utilizan aserciones (`self.assertEqual`, `self.assertTrue`, etc.) para verificar que la respuesta del servidor (código de estado, datos JSON) sea la esperada y que el estado de la base de datos se haya modificado correctamente.
    - **Tipos de Pruebas**:
        - **Pruebas de Endpoints** (ej. `test_endpoints_attendances.py`): Verifican el comportamiento de la API desde el punto de vista de un cliente HTTP, asegurando que cada endpoint responda correctamente a diferentes peticiones.
        - **Pruebas de Lógica de Negocio** (ej. `test_attendance_logic.py`): Se centran en probar directamente los métodos de las clases en el directorio `bussiness_logic`, asegurando que las reglas de negocio se apliquen correctamente, independientemente de la capa de API.


## Endpoints de la API

A continuación se describen los endpoints de la API, agrupados por funcionalidad.

### Autenticación

- **`GET /auth`**: Endpoint de prueba para verificar la disponibilidad del servicio de autenticación.
- **`POST /auth`**: Autentica a un usuario y devuelve un token de acceso.
    - **Body**: `{ "username": "nombre_de_usuario", "password": "contraseña" }`
- **`POST /auth/register`**: Registra un nuevo usuario en el sistema.
    - **Requiere autenticación**: Sí
    - **Body**: `{ "username": "...", "password": "...", "fullname": "...", "rol": "...", "access_level": "..." }`

### Cursos

- **`GET /cursos`**: Obtiene todos los cursos.
    - **Requiere autenticación**: Sí
- **`GET /cursos/preceptor/<preceptor_id>`**: Obtiene todos los cursos a cargo de un preceptor.
    - **Requiere autenticación**: Sí
- **`GET /cursos/<id>`**: Obtiene un curso por su ID.
    - **Requiere autenticación**: Sí
- **`DELETE /cursos/<id>`**: "Elimina" un curso (lo marca como inactivo).
    - **Requiere autenticación**: Sí
- **`POST /cursos/<course_id>/alumno/<student_id>`**: Asocia un alumno a un curso.
    - **Requiere autenticación**: Sí
- **`POST /cursos`**: Crea un nuevo curso.
    - **Requiere autenticación**: Sí
    - **Body**: `{ "nombre": "...", "division": "...", "año": "..." }`
- **`PATCH /cursos/<id>`**: Actualiza un curso existente.
    - **Requiere autenticación**: Sí

### Alumnos

- **`GET /alumnos`**: Obtiene todos los alumnos activos.
    - **Requiere autenticación**: Sí
- **`GET /alumnos/todos`**: Obtiene todos los alumnos (activos e inactivos).
    - **Requiere autenticación**: Sí
- **`GET /alumnos/<id>`**: Obtiene un alumno por su ID.
    - **Requiere autenticación**: Sí
- **`DELETE /alumnos/<id>`**: "Elimina" un alumno (lo marca como inactivo).
    - **Requiere autenticación**: Sí
- **`POST /alumnos`**: Crea un nuevo alumno.
    - **Requiere autenticación**: Sí
- **`PATCH /alumnos/<id>`**: Actualiza un alumno existente.
    - **Requiere autenticación**: Sí
- **`POST /alumnos/<alumno_id>/tutores/<tutor_id>`**: Asocia un tutor a un alumno.
    - **Requiere autenticación**: Sí

### Tutores

- **`GET /tutores`**: Obtiene todos los tutores activos.
    - **Requiere autenticación**: Sí
- **`GET /tutores/<id>`**: Obtiene un tutor por su ID.
    - **Requiere autenticación**: Sí
- **`DELETE /tutores/<id>`**: "Elimina" un tutor (lo marca como inactivo).
    - **Requiere autenticación**: Sí
- **`POST /tutores`**: Crea un nuevo tutor.
    - **Requiere autenticación**: Sí
- **`PATCH /tutores/<id>`**: Actualiza un tutor existente.
    - **Requiere autenticación**: Sí

### Asistencias

- **`GET /asistencias`**: Obtiene todas las asistencias activas.
    - **Requiere autenticación**: Sí
- **`GET /asistencias/inactivas`**: Obtiene todas las asistencias inactivas.
    - **Requiere autenticación**: Sí
- **`GET /asistencias/<id>`**: Obtiene una asistencia por su ID.
    - **Requiere autenticación**: Sí
- **`GET /asistencias/alumno/<id>`**: Obtiene las asistencias de un alumno por su ID, requiere parámetros `start` y `end` en la query string.
    - **Requiere autenticación**: Sí
- **`POST /asistencias/cerrar/<id>`**: Cierra la asistencia de un curso para el día actual.
    - **Requiere autenticación**: Sí
- **`POST /asistencias/revision`**: Obtiene las asistencias de un curso en una fecha específica.
    - **Requiere autenticación**: Sí
    - **Body**: `{ "course_id": "...", "date_to_search": "..." }`
- **`DELETE /asistencias/<id>`**: "Elimina" una asistencia (la marca como inactiva).
    - **Requiere autenticación**: Sí
- **`POST /asistencias`**: Crea una nueva asistencia.
    - **Requiere autenticación**: Sí
- **`PATCH /asistencias/<id>`**: Actualiza una asistencia existente.
    - **Requiere autenticación**: Sí
- **`GET /asistencias/fechas/<course_id>`**: Obtiene las fechas de asistencia disponibles para un curso.
    - **Requiere autenticación**: Sí
