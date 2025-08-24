from telethon import TelegramClient
from dotenv import load_dotenv
import os

from telethon.tl.types import DocumentAttributeVideo

load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
STORAGE_CHAT = os.getenv('STORAGE_CHAT')
STORAGE_CHAT_ID = os.getenv('STORAGE_CHAT_ID')

client = TelegramClient("uploader", API_ID, API_HASH)


async def get_video_id(user_chat_id, filename: str, w: int, h: int, duration: int):
    await client.start(phone=PHONE)
    await client.send_file("@VideoMediaSave_bot", filename, attributes=(DocumentAttributeVideo(duration, w, h, supports_streaming=True),), force_document = False, caption=f"{user_chat_id};{duration};{w};{h}")


async def send_video_telethon(user_chat_id, filename: str, w: int, h: int, duration: int):
    async with client:
        await get_video_id(user_chat_id, filename, w, h, duration)
