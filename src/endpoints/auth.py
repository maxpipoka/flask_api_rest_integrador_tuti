from flask import Response, Blueprint, jsonify, request

from ..models.models import User, db

bp = Blueprint('auth', __name__)

#Definicion endpoint que realiza verificacion de existencia de la url
@bp.route('/auth', methods=['GET'])
def testAuth():
    return Response({'message':'Endpoint de autenticación'}), 200

#Definicion endpoint realiza la autenticación de un usuario
@bp.route('/auth', methods=['POST'])
def loginUser():

    try:
        foundedUser = User.query.filter(User.username == request.json['username']).first()
    except:
        return Response({'message':'No se pudo obtener el usuario'}), 401
    
    if foundedUser:
        if foundedUser.password == request.json['password']:
            return Response({'message':'Usuario autenticado'}), 200
        else:
            return Response({'message':'Contraseña incorrecta'}), 401
        
#Definicion endpoint realiza el registro de un usuario
@bp.route('/auth/register', methods=['POST'])
def registerUser():
    
    try:
        newUser = User(username=request.json['username'], 
                       password=request.json['password'], 
                       fullname=request.json['fullname'], 
                       rol=request.json['rol'])
        db.session.add(newUser)
        db.session.commit()

    except Exception as e:
        return jsonify({'message2': f'Error: {str(e)}'}), 400
    
    return Response({'message':'Usuario registrado'}), 200