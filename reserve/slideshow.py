import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup
from data import bot
from sql import data_media

router = Router()

# 📸 Список фотографий с их подписями
PHOTO_LIST = [[photo[2], photo[3]] for photo in data_media.sql_get_main_prod_photo()]


class SlideShowState(StatesGroup):
    viewing = State()


def get_keyboard(paused=False):
    """Создаёт клавиатуру управления."""
    buttons = [
        [InlineKeyboardButton(text="←", callback_data="prev"),
         InlineKeyboardButton(text="||" if not paused else "ᐅ", callback_data="pause" if not paused else "play"),
         InlineKeyboardButton(text="→", callback_data="next")],
        [ InlineKeyboardButton(text='➔      новинки', callback_data='➔      новинки')]

    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == "/slideshow")
async def start_slideshow(message: Message, state: FSMContext):
    """Запускает слайдшоу без мерцания."""
    if not PHOTO_LIST:
        await message.answer("❌ Нет доступных фотографий для слайдшоу.")
        return

    # Начинаем с первой фотографии
    index = 0
    photo_id, caption = PHOTO_LIST[index]

    # Отправляем первое фото
    msg = await message.answer_photo(photo=photo_id, caption=caption, reply_markup=get_keyboard())
    await message.delete()
    # Сохраняем индекс и состояние автоплея
    await state.set_state(SlideShowState.viewing)
    await state.update_data(index=index, msg_id=msg.message_id, playing=True)

    # Запускаем автоплей с небольшой задержкой, чтобы не было двойного обновления
    await asyncio.sleep(3)
    await asyncio.create_task(autoplay_slideshow(message.chat.id, state))


@router.callback_query(F.data.in_(["prev", "next", "pause", "play"]))
async def slideshow_controls(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие на кнопки управления."""
    data = await state.get_data()
    if "index" not in data:
        await callback.answer("❌ Слайдшоу ещё не запущено.")
        return

    index = data["index"]
    msg_id = data["msg_id"]
    playing = data.get("playing", False)

    if callback.data == "prev":  # ⏮ Назад (строго по списку)
        index = (index - 1) % len(PHOTO_LIST)
    elif callback.data == "next":  # ⏭ Вперёд (строго по списку)
        index = (index + 1) % len(PHOTO_LIST)
    elif callback.data == "pause":  # ⏸ Пауза
        await state.update_data(playing=False)
        await update_photo(callback.message.chat.id, msg_id, index, paused=True)
        await callback.answer("Слайдшоу приостановлено.")
        return
    elif callback.data == "play":  # ▶ Плей
        await state.update_data(playing=True)
        await update_photo(callback.message.chat.id, msg_id, index, paused=False)
        await callback.answer("Слайдшоу возобновлено.")
        await asyncio.create_task(autoplay_slideshow(callback.message.chat.id, state))
        return

    # Обновляем фото
    await state.update_data(index=index)
    await update_photo(callback.message.chat.id, msg_id, index, paused=not playing)
    await callback.answer()


async def update_photo(chat_id: int, message_id: int, index: int, paused=False):
    """Обновляет фотографию в сообщении и меняет кнопки."""
    photo_id, caption = PHOTO_LIST[index]
    try:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(media=photo_id, caption=caption),
            reply_markup=get_keyboard(paused)
        )
    except TelegramBadRequest:
        pass


async def autoplay_slideshow(chat_id: int, state: FSMContext):
    """Автоматически переключает фотографии по порядку."""
    while (await state.get_data()).get("playing", False):
        data = await state.get_data()
        index = (data["index"] + 1) % len(PHOTO_LIST)  # Автоплей идёт по порядку
        msg_id = data["msg_id"]

        await state.update_data(index=index)
        await update_photo(chat_id, msg_id, index)

        await asyncio.sleep(3)  # Интервал автоплея
