import json
import logging
from telegram import Bot
from pydantic import ValidationError

from domain.MaxMessage import MaxMessage


logger = logging.getLogger(__name__)


class MessageHandler:

    def __init__(self, bot: Bot, chat_id: str):
        self.bot = bot
        self.chat_id = chat_id

    async def handle(self, raw_value: bytes):
        try:
            data = json.loads(raw_value.decode("utf-8"))
            max_message = MaxMessage(**data)

        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Invalid message format: {e}")
            return False

        text = max_message.to_telegram_text()

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text
        )

        logger.info(f"Message {max_message.id} sent")
        return True