import os
from aiokafka import AIOKafkaConsumer

KAFKA = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

async def consume_topic(topic: str, group_id: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=KAFKA, group_id=group_id)
    await consumer.start()
    try:
        async for msg in consumer:
            yield msg.value
    finally:
        await consumer.stop()
