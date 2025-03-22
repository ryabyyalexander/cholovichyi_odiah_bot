from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F

from data import admin, bot, del_msg
from filters import IsAdmin
from states.states import State_add_photo

router = Router()

audios: list[str] = []
voices: list[str] = []
documents: list[str] = []
stickers: list[str] = []
animations: list[str] = []


@router.message((F.photo | F.video | F.sticker | F.document | F.voice | F.audio | F.animation),
                IsAdmin, StateFilter(State_add_photo.start))
async def set_media(message: Message, state: FSMContext):
    data = await state.get_data()
    set_photo = data['set_photo']
    ct = message.content_type
    user_id = message.from_user.id
    if ct in ['photo', 'video']:
        if user_id == admin:
            await message.delete()
            path = message.photo[-1].file_id if ct == 'photo' else message.video.file_id
            type_media = 'photo' if ct == 'photo' else 'video'
            if message.caption:
                caption = message.caption
            else:
                caption = ''
            last_media = [type_media, path, caption]
            set_photo.append(last_media)
            await state.update_data(set=set)
            msg = await bot.send_message(admin, 'new media')
            await del_msg(msg, 2)
        else:

            await message.delete()
    elif ct == 'sticker':
        await message.delete()
        sticker = message.sticker.file_id
        msg = await bot.send_sticker(chat_id=message.from_user.id,
                                     sticker=sticker)
        print(*sticker)
        await del_msg(msg, 7)
    elif ct == 'document':
        documents.append(message.document.file_id)
        print(*documents)
    elif ct == 'voice':
        voices.append(message.voice.file_id)
        print(*voices)
    elif ct == 'audio':
        audios.append(message.audio.file_id)
        print(*audios)
    elif ct == 'animation':
        animations.append(message.animation.file_id)
        print(*animations)
