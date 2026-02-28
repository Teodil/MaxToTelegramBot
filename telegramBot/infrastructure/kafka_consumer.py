from aiokafka import AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
import logging



async def create_kafka_consumer(
    bootstrap_servers: str,
    group_id: str,
    topic: str,
) -> AIOKafkaConsumer:

    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )

    await consumer.start()
    return consumer

async def ensure_topic_exists(bootstrap_servers, topic_name: str):
    """Создает топик, если он не существует"""
    admin = AIOKafkaAdminClient(bootstrap_servers=bootstrap_servers)
    await admin.start()
    try:
        existing_topics = await admin.list_topics()
        if topic_name not in existing_topics:
            logging.info(f"Topic '{topic_name}' does not exist. Creating...")
            topic = NewTopic(
                name=topic_name,
                num_partitions=3,       # указываем нужное количество партиций
                replication_factor=1    # replication factor
            )
            await admin.create_topics([topic])
            logging.info(f"Topic '{topic_name}' created")
        else:
            logging.info(f"Topic '{topic_name}' already exists")
    finally:
        await admin.close()