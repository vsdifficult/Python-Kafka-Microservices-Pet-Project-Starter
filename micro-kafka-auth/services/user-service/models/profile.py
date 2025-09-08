from sqlalchemy import Table, Column, String, Text, DateTime
from db.database import metadata
import datetime

profiles_table = Table(
    'profiles', metadata,
    Column('id', String, primary_key=True),
    Column('user_id', String, nullable=False),
    Column('email', String, nullable=False),
    Column('bio', Text, nullable=True),
    Column('avatar_url', String, nullable=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow)
)