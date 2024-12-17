from flask import Response, Blueprint, jsonify, request

from src.utils.decorators import token_required

from ..models.models import User, db

from ..utils.security import generate_token

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
            token = generate_token(foundedUser.id)
            print(token)
            return jsonify({'message': 'Usuario autenticado', 'username': foundedUser.username, 'user_id': foundedUser.id, 'access_level': foundedUser.access_level, 'token': token}), 200
            # return jsonify({'message': 'Usuario autenticado', 'username': foundedUser.username, 'user_id': foundedUser.id, 'access_level': foundedUser.access_level}), 200
        else:
            return Response({'message':'Contraseña incorrecta'}), 401
        
        
#Definicion endpoint realiza el registro de un usuario
@bp.route('/auth/register', methods=['POST'])
@token_required
def registerUser():
    
    try:
        newUser = User(username=request.json['username'], 
                       password=request.json['password'], 
                       fullname=request.json['fullname'], 
                       rol=request.json['rol'],
                       access_level=request.json['access_level'])
        db.session.add(newUser)
        db.session.commit()

    except Exception as e:
        return jsonify({'message2': f'Error: {str(e)}'}), 400
    
    return Response({'message':'Usuario registrado'}), 200