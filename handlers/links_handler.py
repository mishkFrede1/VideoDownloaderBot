from aiogram import types, Router, F
import re

from media_parsers.tiktok.tiktok_handlers import tiktok_link_processing
from media_parsers.instagram.instagram_handlers import instagram_link_processing
from media_parsers.youtube.youtube_handlers import youtube_link_processing

router = Router(name=__name__)


@router.message(F.text.regexp(re.compile(r"^(https?:\/\/)?www\.[a-zA-Z0-9-]+\.(com|net|org)(\/.*)?$")))
async def links_handler(message: types.Message):
    if "youtube.com" in message.text:
        await youtube_link_processing(message)

    elif "instagram.com" in message.text:
        await instagram_link_processing(message)

    elif "tiktok.com" in message.text:
        await tiktok_link_processing(message)