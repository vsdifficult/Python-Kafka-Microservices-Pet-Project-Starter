import os
from aiokafka import AIOKafkaProducer
import json

KAFKA = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
producer = AIOKafkaProducer(bootstrap_servers=KAFKA)

async def send_message(topic: str, payload: dict):
    await producer.send_and_wait(topic, json.dumps(payload).encode('utf-8'))
