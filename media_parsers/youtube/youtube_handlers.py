from aiogram import Router, F, Bot, exceptions
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputFile, URLInputFile

from .youtube_downloader import YoutubeDownloader
from telethon_sender import send_video_telethon
import utils

router = Router(name=__name__)

class YoutubeForm(StatesGroup):
    video_url = State()


@router.message(Command("youtube"))
async def youtube_start(message: Message, state: FSMContext):
    await state.set_state(YoutubeForm.video_url)
    await message.answer(utils.send_link_text)


async def youtube_link_processing(message: Message):
    url = message.text
    try:
        yd = YoutubeDownloader(url)
        video_data = yd.get_video_info()
        video_formats_list = [format for format in video_data['formats'] if format[0] in [144, 360, 480, 720, 1080, 1440, 2160] and format[1] is not None]
        video_formats = []
        resolutions = []
        for format in video_formats_list:
            if format[0] not in resolutions:
                video_formats.append(format)
                resolutions.append(format[0])

        res = []
        line = []
        for i, format in enumerate(sorted(video_formats, reverse=True)):
            if format[1] < 49.5:
                download_type = 1
            else:
                download_type = 0
            # There are 3 download_types:
            #  0 - With telethon sender for big files
            #  1 - Without telethon sender
            #  2 - For audio only files

            btn = InlineKeyboardButton(text=f"{format[0]}p {format[1]}MB", callback_data=f"D|{download_type}|{url}|{format[0]}")
            if i % 2 == 0:
                line = [btn]
                if i == len(video_formats) - 1:
                    res.append(line)
            else:
                line.append(btn)
                res.append(line)
                line = []
        res.append([InlineKeyboardButton(text="🔈 MP3", callback_data=f"D|2|{url}")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=res)
        await message.answer_photo(
            photo=video_data["thumbnail"],
            caption=f"📹 <b>{video_data['title']}</b>\n👤 {video_data['uploader']}\n\n<b>Download formats ↓</b>",
            reply_markup=keyboard
        )

    except Exception as e:
        await message.answer(utils.bad_url)
        print(e)


@router.message(YoutubeForm.video_url)
async def youtube_url_receive(message: Message, state: FSMContext):
    await state.clear()
    await youtube_link_processing(message)


@router.callback_query(F.data.startswith("D"))
async def download_video_by_callback(query: CallbackQuery, bot: Bot):
    elements = query.data.split("|")
    await bot.send_message(chat_id=query.from_user.id, text=utils.please_wait_text)
    yd = YoutubeDownloader(elements[2])
    if elements[1] == '2':
        file_data = yd.download_video_audio_only()
        await bot.send_audio(query.from_user.id, FSInputFile(f"vids/{file_data['title']}"), performer=file_data["uploader"], duration=file_data["duration"])
    else:
        file_data = yd.download_video_by_resolution(elements[3])
        h = int(elements[3])
        w = utils.resolutions_16x9[h]

        filename = f"vids/{file_data['title']}_{elements[3]}.{file_data['ext']}"
        if elements[1] == '0':
            await send_video_telethon(query.from_user.id, filename, w, h, file_data['duration'], )
        else:
            try:
                await bot.send_video(query.from_user.id, FSInputFile(filename), width=w, height=h, duration=file_data['duration'], supports_streaming=True, thumbnail=URLInputFile(file_data['thumbnail']))
            except exceptions.TelegramEntityTooLarge:
                await send_video_telethon(query.from_user.id, filename, w, h, file_data['duration'])


@router.message(F.video)
async def youtube_video_get(message: Message, bot: Bot):
    if message.from_user.id == 863400079 and message.caption:
        data = message.caption.split(";")
        await bot.send_video(
            chat_id=data[0],
            video=message.video.file_id,
            supports_streaming=True,
            width=int(data[2]),
            height=int(data[3]),
            duration=int(data[1])
        )
