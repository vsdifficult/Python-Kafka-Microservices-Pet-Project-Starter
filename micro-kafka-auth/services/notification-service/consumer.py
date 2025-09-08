import os, asyncio, json
from aiokafka import AIOKafkaConsumer
from core.mailer import send_email

KAFKA = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

async def handle_user_registered(payload_json: str):
    payload = json.loads(payload_json)
    email = payload.get('email')
    await send_email(email, "Welcome!", "Спасибо за регистрацию!")

async def start_consumer():
    consumer = AIOKafkaConsumer('user.registered', bootstrap_servers=KAFKA, group_id='notification-service')
    await consumer.start()
    try:
        async for msg in consumer:
            await handle_user_registered(msg.value.decode('utf-8'))
    finally:
        await consumer.stop()
