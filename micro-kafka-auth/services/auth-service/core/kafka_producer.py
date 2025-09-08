import os
from aiokafka import AIOKafkaProducer
import json


KAFKA = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
producer = AIOKafkaProducer(bootstrap_servers=KAFKA)


async def publish_user_registered(payload: dict):
    await producer.send_and_wait('user.registered', json.dumps(payload).encode('utf-8'))