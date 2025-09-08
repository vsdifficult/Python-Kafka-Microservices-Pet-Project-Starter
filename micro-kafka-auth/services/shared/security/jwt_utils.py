import os
import jwt
from datetime import datetime, timedelta

JWT_SECRET = os.getenv('JWT_SECRET', 'dev_secret')

def create_jwt(user_id: str, expires_minutes: int = 60*24):
    payload = {"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
