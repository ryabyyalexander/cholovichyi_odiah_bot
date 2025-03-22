import asyncio
import random

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, CallbackQuery

from data import bot, del_msg, btn

router = Router()


def chunk_list(lst, chunk_size):
    """Вивести з lst послідовні фрагменти розміром chunk_size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


@router.callback_query(F.data == btn['album'])
async def process_sl(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    photos = data['favorites']
    media_files = [i[2] for i in photos]
    random.shuffle(media_files)
    if media_files:
        msg = await callback.message.answer('Загрузка альбома...')

        # Разбиваем список на фрагменты по 10 элементов
        for page_number, chunk in enumerate(chunk_list(media_files, 10), start=1):
            media_group = []
            for index, file_id in enumerate(chunk):
                if index == 0:
                    media_group.append(InputMediaPhoto(media=file_id, caption=f"Страница {page_number}"))
                else:
                    media_group.append(InputMediaPhoto(media=file_id))

            # Отправляем альбом
            await bot.send_chat_action(chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await asyncio.sleep(3)
            await bot.send_media_group(chat_id=callback.message.chat.id, media=media_group)

        await msg.delete()
    else:
        msg = await callback.message.answer('Вы еще не загрузили ни одной фотографии.')
        await del_msg(msg, 3)