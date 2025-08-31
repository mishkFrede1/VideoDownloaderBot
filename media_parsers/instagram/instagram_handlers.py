from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from .instagram_downloader import InstagramDownloader
import utils

router = Router(name=__name__)


class InstagramForm(StatesGroup):
    video_url = State()


@router.message(Command("inst"))
async def instagram_start(message: Message, state: FSMContext):
    await state.set_state(InstagramForm.video_url)
    await message.answer(utils.send_link_text)


async def instagram_link_processing(message: Message):
    await message.answer(utils.please_wait_text)
    url = message.text
    try:
        video_data = InstagramDownloader(url).download_video()
        file = FSInputFile(f"vids/{video_data['title']}")
        await message.answer_video(video=file, caption=f"{video_data['caption']}\n\n👤 {video_data['profile']}", supports_streaming=True)

    except Exception as e:
        await message.answer(utils.bad_url)
        print(e)


@router.message(InstagramForm.video_url)
async def instagram_url_receive(message: Message, state: FSMContext):
    await state.clear()
    await instagram_link_processing(message)