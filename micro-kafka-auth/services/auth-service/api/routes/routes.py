from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from uuid import uuid4
from db.database import get_session
from models.user import users_table
from core.security import hash_password, verify_password, create_jwt
from core.kafka_producer import publish_user_registered
from sqlalchemy import select

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post('/register')
async def register(payload: RegisterRequest):
    async for session in get_session():
        q = select(users_table).where(users_table.c.email == payload.email)
        res = await session.execute(q)
    if res.first():
        raise HTTPException(status_code=400, detail='email exists')


    user_id = str(uuid4())
    hashed = hash_password(payload.password)
    await session.execute(users_table.insert().values(id=user_id, email=payload.email, password=hashed, full_name=payload.full_name))
    await session.commit()
    await publish_user_registered({"user_id": user_id, "email": payload.email})
    return {"user_id": user_id}


@router.post('/login', response_model=AuthResponse)
async def login(payload: LoginRequest):
    async for session in get_session():
        q = select(users_table).where(users_table.c.email == payload.email)
        res = await session.execute(q)
        row = res.first()
        if not row:
            raise HTTPException(status_code=401, detail='invalid credentials')
        user = row[0]
        if not verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail='invalid credentials')
        token = create_jwt(user.id)
        return {"access_token": token}