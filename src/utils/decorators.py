from functools import wraps
from flask import request, jsonify

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