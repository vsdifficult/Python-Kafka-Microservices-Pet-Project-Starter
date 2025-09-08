from sqlalchemy import Table, Column, String, Boolean, DateTime
from db.database import metadata
import datetime

users_table = Table(
    'users', metadata,
    Column('id', String, primary_key=True),
    Column('email', String, unique=True, nullable=False),
    Column('password', String, nullable=False),
    Column('full_name', String, nullable=True),
    Column('is_active', Boolean, default=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow)
)