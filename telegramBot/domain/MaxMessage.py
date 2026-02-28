from typing import List, Optional
from pydantic import BaseModel


class MaxMessage(BaseModel):
    id: str
    chatName: str
    senderName: str
    message: str
    files: Optional[List[str]] = []

    def to_telegram_text(self) -> str:
        text = (
            f"📩 Новое сообщение\n\n"
            f"🆔 ID: {self.id}\n"
            f"💬 Чат: {self.chatName}\n"
            f"👤 Отправитель: {self.senderName}\n\n"
            f"📝 Сообщение:\n{self.message}"
        )

        if self.files:
            files_text = "\n".join([f"📎 {file}" for file in self.files])
            text += f"\n\nФайлы:\n{files_text}"

        return text