import asyncio
from random import shuffle
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from data import bot
from sql import data_media
from states.states import SlideShowState

router = Router()

# 📸 Список фотографий с их подписями
PHOTO_LIST = [[photo[2], photo[3]] for photo in data_media.sql_get_all_photo()]

# Возможные значения циклов, которые можно выбрать
CYCLE_OPTIONS = [3, 4, 5, 7, 10, 33]

# Переменная по умолчанию для количества фото в цикле
CYCLE_DEFAULT = 50


def get_keyboard(paused=False):
    """Создаёт клавиатуру управления с кнопками переключения, выбора цикла и закрытия."""
    control_buttons = [
        InlineKeyboardButton(text="←", callback_data="prev"),
        InlineKeyboardButton(text="||" if not paused else "ᐅ", callback_data="pause" if not paused else "play"),
        InlineKeyboardButton(text="→", callback_data="next")
    ]
    # Кнопки выбора количества циклов
    cycle_buttons = [
        InlineKeyboardButton(text=str(cycle), callback_data=f"setcycle_{cycle}")
        for cycle in CYCLE_OPTIONS
    ]
    close_button = InlineKeyboardButton(text='✖️ закрити', callback_data='✖️ закрити')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        control_buttons,
        cycle_buttons,
        [close_button]
    ])
    return keyboard


@router.message(F.text == "/slider")
async def start_slideshow(message: Message, state: FSMContext):
    """Запускает слайдшоу без мерцания."""
    if not PHOTO_LIST:
        await message.answer("❌ Нет доступных фотографий для слайдшоу.")
        return
    shuffle(PHOTO_LIST)
    # Начинаем с первой фотографии
    index = 0
    photo_id, caption = PHOTO_LIST[index]

    # Отправляем первое фото
    msg = await message.answer_photo(photo=photo_id, reply_markup=get_keyboard())
    await message.delete()
    # Сохраняем индекс, состояние автоплея, счётчик цикла и выбранное количество фото в цикле (по умолчанию CYCLE_DEFAULT)
    await state.set_state(SlideShowState.viewing)
    await state.update_data(index=index, msg_id=msg.message_id, playing=True, cycle_count=0, cycle_length=CYCLE_DEFAULT)

    # Запускаем автоплей с небольшой задержкой
    await asyncio.sleep(3)
    await asyncio.create_task(autoplay_slideshow(message.chat.id, state))


@router.callback_query(F.data.in_(["prev", "next", "pause", "play"]))
async def slideshow_controls(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатия на кнопки управления слайдшоу."""
    data = await state.get_data()
    if "index" not in data:
        await callback.answer("❌ Слайдшоу ещё не запущено.")
        return

    index = data["index"]
    msg_id = data["msg_id"]
    playing = data.get("playing", False)

    if callback.data == "prev":  # Назад
        index = (index - 1) % len(PHOTO_LIST)
        # Сбросим счётчик цикла при ручном переключении
        await state.update_data(index=index, cycle_count=0)
    elif callback.data == "next":  # Вперёд
        index = (index + 1) % len(PHOTO_LIST)
        await state.update_data(index=index, cycle_count=0)
    elif callback.data == "pause":  # Пауза
        await state.update_data(playing=False)
        await update_photo(callback.message.chat.id, msg_id, index, paused=True)
        await callback.answer("Слайдшоу приостановлено.")
        return
    elif callback.data == "play":  # Плей
        await state.update_data(playing=True, cycle_count=0)
        await update_photo(callback.message.chat.id, msg_id, index, paused=False)
        await callback.answer("Слайдшоу возобновлено.")
        await asyncio.create_task(autoplay_slideshow(callback.message.chat.id, state))
        return

    await update_photo(callback.message.chat.id, msg_id, index, paused=not playing)
    await callback.answer()


@router.callback_query(F.data.startswith("setcycle_"))
async def set_cycle_length(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор количества фото в цикле."""
    try:
        new_cycle = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.answer("Неверное значение цикла.")
        return

    # Обновляем сохранённое значение цикла
    await state.update_data(cycle_length=new_cycle, cycle_count=0)
    await callback.answer(f"Цикл установлен на {new_cycle} фото.")
    # Обновляем клавиатуру, чтобы изменения сразу отобразились
    data = await state.get_data()
    chat_id = callback.message.chat.id
    msg_id = data["msg_id"]
    index = data["index"]
    playing = data.get("playing", False)
    await update_photo(chat_id, msg_id, index, paused=not playing)


async def update_photo(chat_id: int, message_id: int, index: int, paused=False):
    """Обновляет фотографию в сообщении и меняет кнопки."""
    photo_id, caption = PHOTO_LIST[index]
    try:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(media=photo_id),
            reply_markup=get_keyboard(paused)
        )
    except TelegramBadRequest:
        pass


async def autoplay_slideshow(chat_id: int, state: FSMContext):
    """
    Автоматически переключает фотографии по порядку, показывая цикл из выбранного количества фото.
    После показа заданного числа фото автоплей останавливается (режим паузы),
    ожидая нажатия кнопки "▶" для возобновления следующего цикла.
    """
    while (await state.get_data()).get("playing", False):
        data = await state.get_data()
        current_index = data["index"]
        msg_id = data["msg_id"]
        cycle_count = data.get("cycle_count", 0)
        cycle_length = data.get("cycle_length", CYCLE_DEFAULT)  # Используем переменную CYCLE_DEFAULT
        next_index = (current_index + 1) % len(PHOTO_LIST)

        # Если достигли конца текущего цикла
        if cycle_count >= cycle_length - 1:
            await state.update_data(index=next_index, playing=False, cycle_count=0)
            await update_photo(chat_id, msg_id, next_index, paused=True)
            break
        else:
            await state.update_data(index=next_index, cycle_count=cycle_count + 1)
            await update_photo(chat_id, msg_id, next_index)

        await asyncio.sleep(3)
