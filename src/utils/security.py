import os

import datetime
import pytz
import jwt


def generate_token(userid = int) -> str:

    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    expiration_minutes = int(os.getenv('TOKEN_EXPIRATION_MINUTES'))
    payload = {
        'iat': datetime.datetime.now(tz=tz),
        'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=expiration_minutes),
        'user': userid,
    }

    return jwt.encode(payload, os.getenv('SECRET_JWT_KEY'), algorithm='HS256')


def decode_token(token: str) -> dict:
    
    splited_token = token.split(' ')[1]

    return jwt.decode(splited_token, os.getenv('SECRET_JWT_KEY'), algorithms=['HS256'])