import asyncio

from pymax import MaxClient
from datetime import datetime

client = MaxClient(
    phone="+79242313280",
    work_dir="cache",  # директория для сессий
)


@client.on_start
async def on_start() -> None:
    print(f"Клиент запущен. Ваш ID: {client.me.id}")
    history = await client.fetch_history(chat_id=-71389173874914) #есть from time для получения сообщений от какой-то метки времени

    #for m in history:
    m = history[-1] #последнее сообщение
    m_dict = m.__dict__
    sender = await client.get_user(m_dict['sender'])
    sender_dict = sender.__dict__
    sender_name = sender_dict['names']
    message = {'id':m_dict['id'],'text':m_dict['text'],'sender':sender_name[0].first_name+" "+sender_name[0].last_name, 'datetime':datetime.fromtimestamp(m_dict['time']/1000).strftime('%Y-%m-%d %H:%M:%S')}
    print(message)


async def main():
    await client.start()  # подключение и авторизация


if __name__ == "__main__":
    asyncio.run(main())