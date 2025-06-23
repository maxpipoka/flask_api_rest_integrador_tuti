from functools import wraps
from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from src.utils.security import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message':'Token is missing!'}), 401
        
        try:
            decode_token(token)
        except:
            return jsonify({'message':'Token invalid!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def require_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.content_type != "application/json":
            return jsonify({"message": "Content-Type must be application/json"}), 415
        if not request.is_json:
            return jsonify({"message": "JSON data is missing or invalid"}), 400
        return f(*args, **kwargs)
    return decorated



def handle_api_exceptions(default_message="Error en la operación"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ValueError as e:
                return jsonify({"message": str(e)}), 404
            except SQLAlchemyError as e:
                return jsonify({"message": f"Database error: {str(e)}"}), 500
            except Exception as e:
                return jsonify({"message": f"{default_message}: {str(e)}"}), 500
        return wrapper
    return decorator