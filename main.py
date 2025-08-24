import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import youtube_commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(youtube_commands.router)
    print("[INFO] Bot has started!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())