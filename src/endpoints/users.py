from datetime import datetime
from flask import Blueprint, jsonify, request

from src.utils.decorators import token_required

from ..models.models import User, db

bp = Blueprint('usuarios', __name__)

#obtencion usuarios
@bp.route('/usuarios', methods=['GET'])
@token_required
def get_users():

    try:
        all_users = User.query.filter(User.active == True).order_by(User.id)
    except Exception as error:
        return jsonify({"message":"No se pudieron obtener usuarios"}), 404
    
    if not all_users:
        return jsonify({"message":"No se pueden obtener los usuarios"}), 400
    
    serialized_users = [user.as_dict() for user in all_users]

    return jsonify(serialized_users), 200


#obtencion usuario por id
@bp.route('/usuarios/<id>', methods=['GET'])
@token_required
def get_user_by_id(id):
    
    try:
        founded_user = db.session.get(User, id)

        if not founded_user:
            return jsonify({"message":"Usuario no encontrado"}), 404
    
    except Exception as e:
        return jsonify({"message":"No se pudo obtener el usuario - {e}"}), 404
    
    serialized_user = founded_user.as_dict()

    return jsonify(serialized_user), 200
    
    

#creacion usuario
@bp.route('/usuarios', methods=['POST'])
@token_required
def save_user():

    new_user = None

    if not request.json:
        return jsonify({"message":"No se proporcionaron datos"}), 400
    
    try:
        new_user = User(username=request.json['username'], 
                        password=request.json['password'], 
                        fullname=request.json['fullname'], 
                        rol=request.json['rol'],
                        access_level=request.json['access_level'])
    
    except KeyError as error:
        return jsonify({"message":f"Error: {str(error)}"}), 400
    
    except Exception as error:
        return jsonify({"message":f"Error: {str(error)}"}), 400
    
    try:
        db.session.add(new_user)
    
    except Exception as error:
        return jsonify({"message":f"Error: {str(error)}"}), 400
    
    try:
        db.session.commit()
        return jsonify({"message":"Usuario registrado"}), 201
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"message":f"Error: {str(error)}"}), 400

#edicion usuario
@bp.route('/usuarios/<id>', methods=['PATCH'])
@token_required
def update_user(id):
    
    try:
        founded_user = db.session.get(User, id)

    except Exception as error:
        return jsonify({"message":f"No se pudo obtener el usuario - {str(error)}"}), 404
    
    if not founded_user:
        return jsonify({"message":"Usuario no encontrado"}), 404
    
    try:
        data = request.get_json()
    
    except Exception as error:
        return jsonify({"message":f"Error, no hay informacion para actualizar el usuaario - {str(error)}"}), 400
    
    try:
        update = False

        if 'username' in data:
            founded_user.username = data['username']
            update = True
        
        if 'password' in data:
            founded_user.password = data['password']
            update = True

        if 'fullname' in data:
            founded_user.fullname = data['fullname']
            update = True

        if 'rol' in data:
            founded_user.rol = data['rol']
            update = True

        if 'access_level' in data:
            founded_user.access_level = data['access_level']
            update = True

        if update:
            founded_user.updated_at = datetime.now()
        
        db.session.commit()

    except Exception as error:
        db.session.rollback()
        return jsonify({"message":f"Error: {str(error)}"}), 400
    
    serialized_user = founded_user.as_dict()

    return jsonify(serialized_user), 201

#eliminacion usuario
@bp.route('/usuarios/<id>', methods=['DELETE'])
@token_required
def delete_user(id):
    
    try:
        founded_user = db.session.get(User, id)

    except Exception as error:
        return jsonify({"message":f"No se pudo obtener el usuario - {str(error)}"}), 400
    
    try:
        founded_user.active = False
        founded_user.updated_at = datetime.now()
        db.session.commit()

    except Exception as error:
        db.session.rollback()
        return jsonify({"message":f"Error: {str(error)}"}), 400
    
    return jsonify(founded_user.as_dict()), 201
