from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from .tiktok_downloader import TiktokDownloader
import utils

router = Router(name=__name__)

class TiktokForm(StatesGroup):
    video_url = State()


@router.message(Command("tiktok"))
async def tiktok_start(message: Message, state: FSMContext):
    await state.set_state(TiktokForm.video_url)
    await message.answer(utils.send_link_text)


async def tiktok_link_processing(message: Message):
    await message.answer(utils.please_wait_text)
    url = message.text
    try:
        video_title = TiktokDownloader(url).download_video()
        await message.answer_video(FSInputFile(f"vids/{video_title}"), supports_streaming=True)

    except Exception as e:
        await message.answer(utils.bad_url)
        print(e)


@router.message(TiktokForm.video_url)
async def youtube_url_receive(message: Message, state: FSMContext):
    await state.clear()
    await tiktok_link_processing(message)