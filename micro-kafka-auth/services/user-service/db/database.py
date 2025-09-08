import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://auth:authpass@postgres_auth:5432/authdb')
engine = create_async_engine(DATABASE_URL, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
metadata = MetaData()


async def get_session():
    async with async_session() as s:
        yield s