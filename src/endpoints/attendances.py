from datetime import datetime

from flask import Response, Blueprint, request, jsonify

from ..models.models import Attendance, db

bp= Blueprint('asistencias', __name__)

# Definicion endpoint obtiene las asistencias
@bp.route('/asistencias', methods=['GET'])
def getAttendances():
    
    try:
        allAttendances = Attendance.query.filter(Attendance.active == True).order_by(Attendance.id)

    except:
        return Response({'message':'No se pueden obtener las asistencias'}), 400
    
    if not allAttendances:
        return Response({'message':'No se pueden obtener las asistencias'}), 400
    
    serialized_attendances = [attendance.as_dict() for attendance in allAttendances]

    return jsonify(serialized_attendances), 200


# Definicion endpoint obtencion una asistencia por id
@bp.route('/asistencia/<int:id>', methods=['GET'])
def getAttendanceById(id):

    try:
        foundAttendance = Attendance.query.get(id)

    except:
        return Response({'message':'No se pudo obtener la asistencia'}), 400
    
    if not foundAttendance:
        return Response({'message':'No se pudo obtener la asistencia'}), 400
    
    serialized_attendance = [foundAttendance.as_dict()]

    return jsonify(serialized_attendance),200


# Definicion endpoint borrado de asistencia, cambio el activo
@bp.route('/asistencia/<int:id>', methods=['DELETE'])
def deleteAttendance(id):

    try:
        foundAttendance = Attendance.query.get(id)

    except:
        return Response({'message':'No se pudo obtener la asistencia'}), 400
    
    try:
        foundAttendance.active = False
        foundAttendance.updatedAt = datetime.now()
        db.session.commit()

    except:
        db.session.rollback() # Revertir la transacción en caso de error
        return Response({'message':'No se pudo borrar la asistencia'}), 400
    
    serialized_attendance = [foundAttendance.as_dict()]

    return jsonify(serialized_attendance), 200


# Definicion endpoint creacion asistencia
@bp.route('/asistencia', methods=['POST'])
def saveAttendance():

    newAttendance = None

    if not request.json:
        return Response({'message':'JSON data is missing of invalid'}), 400
    
    try:
        newAttendance: Attendance(
            course_id = request.json['course_id'],
            student_id = request.json['student_id'],
            day = datetime.now(),
            state = request.json['state'],
            active = request.json['active']
        )

    except KeyError as e:
        return jsonify({'message1': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'message2': f'Error: {str(e)}'}), 400
    except:
        return jsonify({'message3':'No se puede crear la instancia'}), 400
    
    try:
        db.session.add(newAttendance)

    except:
        return Response({'message':'No se pudo ADD asistencia'}), 400
    
    try:
        # Confirmacion de las operaciones creadas en la sesion
        db.session.commit()
        return Response({'message': 'success'}), 201
    
    except:
        return Response({'message': 'No se puede commit'}), 400
    

# Definicion endpoint edicion asistencia
@bp.route('/asistencia/<int:id>', methods=['PATCH'])
def updateAttendance(id):

    try:
        foundAttendance = Attendance.query.get(id)

    except:
        return Response({'message': 'No se puede obtener la asistencia'}), 400
    
    if not foundAttendance:
        return Response({'message': 'No se puede obtener el curso'}), 400
    
    try:
        data = request.get_json()
    except:
        return Response({'message': 'JSON data is missing or invalid'}), 400
    
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
        return Response({'message':'Error al modificar los campos de la asistencia: ' + str(e)}), 500
    
    serialized_attendance = foundAttendance.as_dict()

    return jsonify(serialized_attendance), 200