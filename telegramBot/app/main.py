import os
import asyncio
import logging
import signal

from telegram import Bot

from infrastructure.kafka_consumer import create_kafka_consumer, ensure_topic_exists
from application.message_handler import MessageHandler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
KAFKA_BOOTSTRAP_SERVERS = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_GROUP_ID = os.environ["KAFKA_GROUP_ID"]
CHAT_ID = os.environ["CHAT_ID"]


shutdown_event = asyncio.Event()


def shutdown():
    logging.info("Shutdown signal received")
    shutdown_event.set()


async def consume():
    bot = Bot(token=TELEGRAM_TOKEN)
    handler = MessageHandler(bot, CHAT_ID)

    await ensure_topic_exists(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        topic_name=KAFKA_TOPIC
    )

    consumer = await create_kafka_consumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        topic=KAFKA_TOPIC,
    )

    try:
        async for msg in consumer:
            if shutdown_event.is_set():
                break

            success = await handler.handle(msg.value)

            if success:
                await consumer.commit()

    finally:
        await consumer.stop()
        logging.info("Kafka consumer stopped")


async def main():
    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGTERM, shutdown)
    loop.add_signal_handler(signal.SIGINT, shutdown)

    await consume()


if __name__ == "__main__":
    asyncio.run(main())