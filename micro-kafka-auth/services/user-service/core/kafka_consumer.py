import os, asyncio, json
from aiokafka import AIOKafkaConsumer
from db.database import get_session
from models.profile import profiles_table
from sqlalchemy import insert

KAFKA = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

async def handle_user_registered(payload_json: str):
    payload = json.loads(payload_json)
    user_id = payload.get('user_id')
    email = payload.get('email')
    async for session in get_session():
        stmt = insert(profiles_table).values(id=user_id, user_id=user_id, email=email, bio=None)
        try:
            await session.execute(stmt)
            await session.commit()
        except Exception:
            await session.rollback()


async def consumer_task():
    consumer = AIOKafkaConsumer('user.registered', bootstrap_servers=KAFKA, group_id='user-service-group')
    await consumer.start()
    try:
        async for msg in consumer:
            await handle_user_registered(msg.value.decode('utf-8'))
    finally:
        await consumer.stop()