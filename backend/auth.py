
# backend/auth.py
import os
import time
from typing import Optional
import jwt
from fastapi import HTTPException, Depends, Header
from pydantic import BaseModel
from pymongo import MongoClient

SECRET = os.environ.get('JWT_SECRET', 'dev-secret-change-me')
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client.get_default_database() or client['assistant_db']

class DeviceRecord(BaseModel):
    device_id: str
    owner: str
    name: Optional[str] = None
    created_at: float = time.time()

def create_token(device_id: str, owner: str, expires_sec: int = 3600):
    payload = {
        'device_id': device_id,
        'owner': owner,
        'exp': int(time.time()) + expires_sec
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token

def verify_token(auth_header: Optional[str] = Header(None)):
    if not auth_header:
        raise HTTPException(status_code=401, detail='Authorization header missing')
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail='Invalid auth scheme')
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

def register_device(device_id: str, owner: str, name: str | None = None):
    rec = {'device_id': device_id, 'owner': owner, 'name': name, 'created_at': time.time()}
    db.devices.update_one({'device_id': device_id}, {'$set': rec}, upsert=True)
    return rec

def get_device(device_id: str):
    return db.devices.find_one({'device_id': device_id})


def decode_token(token: str):
    import jwt
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return payload
    except Exception as e:
        raise
