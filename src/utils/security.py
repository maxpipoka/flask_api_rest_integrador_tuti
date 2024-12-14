import os

import datetime
import pytz
import jwt


def generate_token(userid = int) -> str:

    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    payload = {
        'iat': datetime.datetime.now(tz=tz),
        'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(hours=1),
        'user': userid,
    }

    return jwt.encode(payload, os.getenv('SECRET_JWT_KEY'), algorithm='HS256')


def decode_token(token: str) -> dict:
    
    splited_token = token.split(' ')[1]

    return splited_token.decode(token, os.getenv('SECRET_JWT_KEY'), algorithms=['HS256'])