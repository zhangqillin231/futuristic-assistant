
# backend/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..auth import create_token, register_device, get_device

router = APIRouter(prefix='/auth')

class RegisterRequest(BaseModel):
    device_id: str
    owner: str
    name: str | None = None

@router.post('/register')
async def register(req: RegisterRequest):
    rec = register_device(req.device_id, req.owner, req.name)
    token = create_token(req.device_id, req.owner, expires_sec=60*60*24*30)  # 30 days
    return {'device': rec, 'token': token}

@router.get('/device/{device_id}')
async def get_device_info(device_id: str):
    rec = get_device(device_id)
    if not rec:
        raise HTTPException(status_code=404, detail='device_not_found')
    return rec
