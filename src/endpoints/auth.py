from flask import Blueprint, jsonify, request

from src.utils.decorators import token_required

from ..models.models import User, db

from ..utils.security import generate_token

bp = Blueprint('auth', __name__)

#Definicion endpoint que realiza verificacion de existencia de la url
@bp.route('/auth', methods=['GET'])
def test_auth():
    return jsonify({'message':'Endpoint de autenticación'}), 200

#Definicion endpoint realiza la autenticación de un usuario
@bp.route('/auth', methods=['POST'])
def login_user():

    try:
        founded_user = User.query.filter(User.username == request.json['username']).first()
    except Exception as e:
        return jsonify({'message':'No se pudo obtener el usuario', 'error': str(e)}), 500
    
    if founded_user is None:
        return jsonify({'message':'Usuario no encontrado'}), 404
    
    if founded_user:
        if founded_user.password == request.json['password']:
            token = generate_token(founded_user.id)
            return jsonify({'message': 'Usuario autenticado', 'username': founded_user.username, 'user_id': founded_user.id, 'access_level': founded_user.access_level, 'token': token}), 200
        else:
            return jsonify({'message':'Contraseña incorrecta'}), 401
        
        
#Definicion endpoint realiza el registro de un usuario
@bp.route('/auth/register', methods=['POST'])
@token_required
def register_user():
    
    try:
        new_user = User(username=request.json['username'], 
                       password=request.json['password'], 
                       fullname=request.json['fullname'], 
                       rol=request.json['rol'],
                       access_level=request.json['access_level'])
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400
    
    return jsonify({'message':'Usuario registrado'}), 201