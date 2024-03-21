from jwt import encode, decode
from jwt import exceptions
import os
from datetime import datetime, timedelta
from flask import jsonify

try:
    secret = os.environ['SECRET']
except Exception as e:
    print(f"no se pudo encontrar el secreto en las variables de entorno: {e}")


def expire_date(days: int):
    now = datetime.now()
    newDate = now + timedelta(days)
    return newDate


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(1)},
                   key=secret
, algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(token, output= False):
    try:
        if output:
            return decode(token, key=secret
, algorithms=["HS256"])
            
        decode(token, key=secret
, algorithms=["HS256"])
        
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token expired"})
        response.status_code = 401
        return response
    