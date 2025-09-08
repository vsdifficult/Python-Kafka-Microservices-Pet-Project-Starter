from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from db.database import get_session
from models.profile import profiles_table
from sqlalchemy import select, update

router = APIRouter()

class ProfileOut(BaseModel):
    id: str
    user_id: str
    email: str
    bio: str | None = None
    avatar_url: str | None = None

class ProfileUpdate(BaseModel):
    bio: str | None = None
    avatar_url: str | None = None

@router.get("/profile/{user_id}", response_model=ProfileOut)
async def get_profile(user_id: str):
    async for session in get_session():
        q = select(profiles_table).where(profiles_table.c.user_id == user_id)
        res = await session.execute(q)
        row = res.first()
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        p = row[0]
        return ProfileOut(
            id=p.id,
            user_id=p.user_id,
            email=p.email,
            bio=p.bio,
            avatar_url=p.avatar_url
        )

@router.put("/profile/{user_id}", response_model=ProfileOut)
async def update_profile(user_id: str, payload: ProfileUpdate):
    async for session in get_session():
        stmt = (
            update(profiles_table)
            .where(profiles_table.c.user_id == user_id)
            .values(bio=payload.bio, avatar_url=payload.avatar_url)
            .returning(profiles_table)
        )
        res = await session.execute(stmt)
        await session.commit()
        row = res.first()
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        p = row[0]
        return ProfileOut(
            id=p.id,
            user_id=p.user_id,
            email=p.email,
            bio=p.bio,
            avatar_url=p.avatar_url
        )

@router.get("/profiles", response_model=List[ProfileOut])
async def list_profiles():
    async for session in get_session():
        q = select(profiles_table)
        res = await session.execute(q)
        profiles = [ProfileOut(
            id=p.id,
            user_id=p.user_id,
            email=p.email,
            bio=p.bio,
            avatar_url=p.avatar_url
        ) for p, in res.fetchall()]
        return profiles
