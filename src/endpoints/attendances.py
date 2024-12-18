from datetime import datetime

from flask import Blueprint, request, jsonify

from src.utils.decorators import token_required

from ..models.models import Attendance, Course, Student, db

bp= Blueprint('asistencias', __name__)

# Definicion endpoint obtiene las asistencias
@bp.route('/asistencias', methods=['GET'])
@token_required
def getAttendances():
    
    try:
        allAttendances = Attendance.query.filter(Attendance.active == True).order_by(Attendance.id)

    except:
        print('404 - No se pueden obtener las asistencias')
        return jsonify({'message':'No se pueden obtener las asistencias'}), 404
    
    if not allAttendances:
        print('400 - No se pueden obtener las asistencias')
        return jsonify({'message':'No se pueden obtener las asistencias'}), 400
    
    serialized_attendances = [attendance.as_dict() for attendance in allAttendances]

    print('200 - Asistencias obtenidas')
    return jsonify(serialized_attendances), 200


# Definicion endpoint obtiene las asistencias inactivas
@bp.route('/asistencias/inactivas', methods=['GET'])
@token_required
def getInactiveAttendances():
    
    try:
        allAttendances = Attendance.query.filter(Attendance.active == False).order_by(Attendance.id)

    except:
        print('404 - No se pueden obtener las asistencias')
        return jsonify({'message':'No se pueden obtener las asistencias'}), 404
    
    if not allAttendances:
        print('400 - No se pueden obtener las asistencias')	
        return jsonify({'message':'No se pueden obtener las asistencias'}), 400
    
    serialized_attendances = [attendance.as_dict() for attendance in allAttendances]

    print('200 - Asistencias inactivas obtenidas')
    return jsonify(serialized_attendances), 200


# Definicion endpoint para cerra asistencia de un curso en un dia
@bp.route('/asistencias/cerrar/<int:id>', methods=['POST'])
@token_required
def closeAttendance(id):

    current_date = datetime.now().date()
    attendances_id = []

    try:
        foundedCourse = Course.query.get(id)
        allAttendances = Attendance.query.filter(
             db.cast(Attendance.day, db.Date) == current_date).filter(
            Attendance.course_id==id
            )
        
        for attendance in allAttendances:
            attendances_id.append(attendance.student_id)

    except:
        print('404 - No se pudo obtener el curso y asistencias')
        return jsonify({'message':'No se pudo obtener el curso y asistencias'}), 404
    
    try:
        for student in foundedCourse.students:
            if student.id not in attendances_id:
                newAttendance = Attendance(
                    course_id = id,
                    student_id = student.id,
                    state = False,
                    active = True,
                    day = current_date
                )

                db.session.add(newAttendance)
        
        db.session.commit()

        print('200 - Asistencia cerrada')
        return jsonify({'message':'Asistencia cerrada'}), 200
    
    except:
        print('400 - No se pudo cerrar la asistencia')
        return jsonify({'message':'No se pudo comprobar la asistencia'}), 400


# Definicion endpoint obtencion de asistencias de un dia y un curso
@bp.route('/asistencias/revision/', methods=['POST'])
@token_required
def getAttendaceByDayAndCourse():
    course_id = request.json['course_id']
    date_to_search = request.json['date_to_search']
    founded_attendances = None
    attendances_response = []

    if not course_id or not date_to_search:
        print('400 - No se recibio course_id o date_to_search')
        return jsonify({'message': 'No se recibio course_id o date_to_search'}), 400
    
    try:
        founded_attendances = Attendance.query.filter(
            Attendance.course_id == course_id).filter(
            db.cast(Attendance.day, db.Date) == date_to_search).all()

    except:
        print('400 - No se pudo buscar las asistencias')
        return jsonify({'message':'No se pudo buscar las asistencias'}), 400
    
    if not founded_attendances:
        print('400 - No se obtuvieron asistencias')
        return jsonify({'message':'No se obtuvieron asistencias'}), 400
    
    if founded_attendances:
        for attendance in founded_attendances:
            attendance_dict = {}
            temp_student = Student.query.get(attendance.student_id)
            attendance_dict['names'] = temp_student.names
            attendance_dict['surnames'] = temp_student.surnames
            attendance_dict['state'] = attendance.state

            attendances_response.append(attendance_dict)

    print('200 - Asistencias de 1 dia y 1 curso obtenidas')
    return jsonify(attendances_response), 200


# Definicion endpoint obtencion una asistencia por id
@bp.route('/asistencias/<int:id>', methods=['GET'])
@token_required
def getAttendanceById(id):

    try:
        foundAttendance = Attendance.query.get(id)

    except:
        print('404 - No se pudo obtener la asistencia')
        return jsonify({'message':'No se pudo obtener la asistencia'}), 404
    
    if not foundAttendance:
        print('400 - No se pudo obtener la asistencia')
        return jsonify({'message':'No se pudo obtener la asistencia'}), 400
    
    serialized_attendance = [foundAttendance.as_dict()]

    print('200 - Asistencia por id obtenida')
    return jsonify(serialized_attendance),200


# Definicion endpoint borrado de asistencia, cambio el activo
@bp.route('/asistencias/<int:id>', methods=['DELETE'])
@token_required
def deleteAttendance(id):

    try:
        foundAttendance = Attendance.query.get(id)

    except:
        print('404 - No se pudo obtener la asistencia')
        return jsonify({'message':'No se pudo obtener la asistencia'}), 404
    
    try:
        foundAttendance.active = False
        foundAttendance.updatedAt = datetime.now()
        db.session.commit()

    except:
        db.session.rollback() # Revertir la transacción en caso de error
        print('400 - No se pudo borrar la asistencia')
        return jsonify({'message':'No se pudo borrar la asistencia'}), 400
    
    serialized_attendance = [foundAttendance.as_dict()]

    print('200 - Asistencia borrada')
    return jsonify(serialized_attendance), 200


# Definicion endpoint creacion asistencia
@bp.route('/asistencias', methods=['POST'])
@token_required
def saveAttendance():

    print(request)

    newAttendance = None
    foundedAttendance = None

    if not request.json:
        print('400 - JSON data is missing or invalid')
        return jsonify({'message':'JSON data is missing of invalid'}), 400
    
    if not request.is_json:
        print('400 - JSON data is missing or invalid')
        return jsonify({'message':'JSON data is missing of invalid'}), 400
    
    if request.content_type != 'application/json':
        print('415 - Content-Type must be application/json')
        return jsonify({'message':'Content-Type must be application/json'}), 415
    

    current_date = datetime.now().date()

    # Comprobación de no guardado de una asistencia para el mismo alumno
    # mismo curso y mismo dia.
    try:
        foundedAttendance = Attendance.query.filter(
            db.cast(Attendance.day, db.Date) ==current_date).filter(
            Attendance.student_id == request.json['student_id']).filter(
            Attendance.course_id == request.json['course_id'])

        serialized_attendances = [attendance.as_dict() for attendance in foundedAttendance]
        
        if serialized_attendances:
            print('406 - Asistencia ya registrada')
            return jsonify({'message':'Asistencia ya registrada'}), 406
    except:
        pass
    
    try:
        newAttendance = Attendance(
            course_id = request.json['course_id'],
            student_id = request.json['student_id'],
            state = request.json['state'],
            active = request.json['active'],
            day = datetime.now()
        )

    except KeyError as e:
        print('400 -' f'Missing field: {e.args[0]}')
        return jsonify({'message1': f'Missing field: {e.args[0]}'}), 400
    
    except Exception as e:
        print('400 -' f'Error: {str(e)}')
        return jsonify({'message2': f'Error: {str(e)}'}), 400
    
    except:
        print('400 - No se puede crear la instancia')
        return jsonify({'message3':'No se puede crear la instancia'}), 400
    
    try:
        db.session.add(newAttendance)

    except:
        print('400 - No se pudo ADD asistencia')
        return jsonify({'message':'No se pudo ADD asistencia'}), 400
    
    try:
        # Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        print('201 - Asistencia creada')
        return jsonify({'message': 'success'}), 201
    
    except:
        print('400 - No se puede commit')
        return jsonify({'message': 'No se puede commit'}), 400
    

# Definicion endpoint edicion asistencia
@bp.route('/asistencias/<int:id>', methods=['PATCH'])
@token_required
def updateAttendance(id):

    try:
        foundAttendance = Attendance.query.get(id)

    except:
        print('404 - No se puede obtener la asistencia')
        return jsonify({'message': 'No se puede obtener la asistencia'}), 404
    
    if not foundAttendance:
        print('400 - No se puede obtener la asistencia a editar')
        return jsonify({'message': 'No se puede obtener la asistencia a editar'}), 400
    
    try:
        data = request.get_json()
    except:
        print('400 - JSON data is missing or invalid')
        return jsonify({'message': 'JSON data is missing or invalid'}), 400
    
    try:
        updated = False

        if 'state' in data:
            foundAttendance.state = data['state']
            updated = True
        if 'day' in data:
            foundAttendance.day = data['day']
            updated = True
        if 'active' in data:
            foundAttendance.active = data['active']
            updated = True

        if updated:
            foundAttendance.updatedAt = datetime.now()

        db.session.commit()

    except Exception as e:
        db.session.rollback() # Reversion transaccion
        print('500 - Error al modificar los campos de la asistencia: ' + str(e))
        return jsonify({'message':'Error al modificar los campos de la asistencia: ' + str(e)}), 500
    
    serialized_attendance = foundAttendance.as_dict()

    return jsonify(serialized_attendance), 200