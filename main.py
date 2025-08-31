import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from media_parsers.tiktok import tiktok_handlers
from media_parsers.youtube import youtube_handlers
from media_parsers.instagram import instagram_handlers
from handlers import links_handler

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(
        youtube_handlers.router,
        instagram_handlers.router,
        tiktok_handlers.router,
        links_handler.router,
    )
    print("[INFO] Bot has started!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())