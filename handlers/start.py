import asyncio
from random import shuffle
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, CallbackQuery
from aiogram import Router, F
from data import admins, bot
from data.functions import start_info, data_time, get_usd_exchange_rate
from data.lexicon import intro, caption_intro, rest
from handlers.slideshow import get_keyboard
from keyboards.ikb import simple_ikb
from sql import data_users, data_product, data_media
from states.states import State_album, SlideShowState

router = Router()

PHOTO_LIST = [[photo[2], photo[3]] for photo in data_media.sql_get_all_photo()]


# def get_keyboard(paused=False):
#     """Создаёт клавиатуру управления."""
#     buttons = [
#         [InlineKeyboardButton(text="←", callback_data="prev"),
#          InlineKeyboardButton(text="||" if not paused else "ᐅ", callback_data="pause" if not paused else "play"),
#          InlineKeyboardButton(text="→", callback_data="next")],
#         [InlineKeyboardButton(text='➔      новинки', callback_data='➔      новинки'), InlineKeyboardButton(text='✖️ закрити', callback_data='✖️ закрити')]
#
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == '/start')
async def process_start_command(message: Message, state: FSMContext):
    # 📸 Список фотографий с их подписями
    shuffle(PHOTO_LIST)

    # получаем данные от пользователя
    user_id = int(message.from_user.id)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.username
    # обновляем статус "блокировки" на 0
    data_users.update_user_blocked(user_id, 0)
    # если юзера с id нет, то создаём запись и возвращаем True, если есть - возвращаем False - "не первый раз"
    data_users.sql_new_user(user_id, first_name, last_name, user_name,
                            True if user_id in admins else False)
    # получаем статистику каталога и формируем каптион для старта
    list_capt = start_info()
    await state.set_state(State_album.start)
    caption_start_info = "\n".join(list_capt)
    # получаем количество рестартов
    restart_count = data_users.get_restart_count(user_id)
    # обновляем количество рестартов + 1
    await state.update_data(restart_count=restart_count)
    formatted_date = data_time()
    usd_rate = get_usd_exchange_rate()

    shuffle(rest)

    if restart_count < 1:
        await message.answer(text="""

🚶🏻👫    🏃🏻‍♂️🚶🏻   🚘🚖  👫🚶🏻👫
М⭕️ДНИЙ ШОПІНГ В  ОДЕСІ""")

    else:
        await message.answer(text = f'{rest[0]}'
        )

    # выполняем первый СТАРТ - запуск ИНТРО
    if restart_count < 1000:
        data_users.update_restart_count(user_id)
        try:
            captions = caption_intro.split('\n')
            video = intro
            current_caption = captions[0]

            msg = await message.answer_video(video=video,
                                             caption=f'''
                                             
{current_caption}

<code>{formatted_date}
в наявності:</code>

{caption_start_info}

<b>1 долл - {round(usd_rate, 2)} UAH</b>   <i>(з сайту НБУ)</i>
''', reply_markup=simple_ikb(2, '➔      новинки', '✖️ закрити'))

            await message.delete()
            k = 0
            while True:
                k = (k + 1) % len(captions)
                await asyncio.sleep(2)
                new_caption = captions[k]
                try:
                    await bot.edit_message_caption(
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        caption=f'''
{new_caption}

<code>{formatted_date}
в наявності:</code>   
                       
{caption_start_info}

<b>1 долл - {round(usd_rate, 2)} UAH</b>   <i>(з сайту НБУ)</i>
''', reply_markup=simple_ikb(2, '➔      новинки', '✖️ закрити'))
                except TelegramBadRequest:
                    pass
                    break  # Выход из цикла при ошибке

        except TelegramBadRequest:
            pass
        #    else:
        #         capt = f"""<code>{formatted_date}
        # </code>
        # {caption_start_info}
        #
        # <code>1 долл - {round(usd_rate, 2)} UAH</code>"""
        #
        #         """Запускает слайдшоу без мерцания."""
        #         if not PHOTO_LIST:
        #             await message.answer("❌ Нет доступных фотографий для слайдшоу.")
        #             return
        #
        #         # Начинаем с первой фотографии
        #         index = 0
        #         photo_id, caption = PHOTO_LIST[index]
        #
        #         # Отправляем первое фото
        #         msg = await message.answer_photo(photo=photo_id, caption=capt, reply_markup=get_keyboard())
        #         await message.delete()
        #         # Сохраняем индекс и состояние автоплея
        #         await state.set_state(SlideShowState.viewing)
        #         await state.update_data(index=index, msg_id=msg.message_id, playing=True)
        #
        #         # Запускаем автоплей с небольшой задержкой, чтобы не было двойного обновления
        #         await asyncio.sleep(3)
        #         await asyncio.create_task(autoplay_slideshow(message.chat.id, state))
        #
        #         await message.delete()

        data_users.update_restart_count(user_id)


# @router.callback_query(F.data.in_(["prev", "next", "pause", "play"]))
# async def slideshow_controls(callback: CallbackQuery, state: FSMContext):
#     """Обрабатывает нажатие на кнопки управления."""
#     data = await state.get_data()
#     if "index" not in data:
#         await callback.answer("❌ Слайдшоу ещё не запущено.")
#         return
#
#     index = data["index"]
#     msg_id = data["msg_id"]
#     playing = data.get("playing", False)
#
#     if callback.data == "prev":  # ⏮ Назад (строго по списку)
#         index = (index - 1) % len(PHOTO_LIST)
#     elif callback.data == "next":  # ⏭ Вперёд (строго по списку)
#         index = (index + 1) % len(PHOTO_LIST)
#     elif callback.data == "pause":  # ⏸ Пауза
#         await state.update_data(playing=False)
#         await update_photo(callback.message.chat.id, msg_id, index, paused=True)
#         await callback.answer("Слайдшоу приостановлено.")
#         return
#     elif callback.data == "play":  # ▶ Плей
#         await state.update_data(playing=True)
#         await update_photo(callback.message.chat.id, msg_id, index, paused=False)
#         await callback.answer("Слайдшоу возобновлено.")
#         await asyncio.create_task(autoplay_slideshow(callback.message.chat.id, state))
#         return
#
#     # Обновляем фото
#     await state.update_data(index=index)
#     await update_photo(callback.message.chat.id, msg_id, index, paused=not playing)
#     await callback.answer()


# async def update_photo(chat_id: int, message_id: int, index: int, paused=False):
#     """Обновляет фотографию в сообщении и меняет кнопки."""
#     photo_id, caption = PHOTO_LIST[index]
#     formatted_date = data_time()
#     usd_rate = get_usd_exchange_rate()
#     list_capt = start_info()
#     caption_start_info = "\n".join(list_capt)
#     capt = f"""<code>{formatted_date}
# </code>
# {caption_start_info}
#
# <code>1 долл - {round(usd_rate, 2)} UAH</code>"""
#     try:
#         await bot.edit_message_media(
#             chat_id=chat_id,
#             message_id=message_id,
#             media=InputMediaPhoto(media=photo_id, caption=capt),  # Добавил caption
#             reply_markup=get_keyboard(paused)
#         )
#     except TelegramBadRequest:
#         pass
#
#
# async def autoplay_slideshow(chat_id: int, state: FSMContext):
#     """Автоматически переключает фотографии по порядку."""
#     while (await state.get_data()).get("playing", False):
#         data = await state.get_data()
#
#         # Проверяем, остановлено ли слайдшоу
#         if not data.get("playing", False):
#             break
#
#         index = (data["index"] + 1) % len(PHOTO_LIST)  # Автоплей идёт по порядку
#         msg_id = data["msg_id"]
#
#         await state.update_data(index=index)
#         await update_photo(chat_id, msg_id, index)
#
#         await asyncio.sleep(3)  # Интервал автоплея


@router.message(F.text.lower().in_(['==']))
async def process_total_command(message: Message):
    await message.delete()
    formatted_date = data_time()
    results = data_product.get_total_products()[1:]

    # Формируем строку для вывода
    output = []
    for row in results:
        if row[0] == 'ИТОГО':
            # Добавляем общее количество товаров после "ИТОГО"
            output.append(f"{row[0]}\t\t\t{row[4]}\nКоличество единиц: {row[2]}\n{formatted_date}")
        else:
            # Убираем строку с "www" из названия товара
            name = row[1].split('\n')[0]  # Берем только первую строку (название товара)
            # Добавляем категорию перед именем товара
            output.append(f"{row[0]} - {name}\t - {row[2]}\t * {row[3]}\t = {row[4]}")

    # Отправляем сообщение с результатами
    await message.answer("\n".join(output), reply_markup=simple_ikb(1, '✖️ закрити'))


@router.callback_query(F.data.in_(['✖️ закрити']))
async def process_sl(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает закрытие слайдшоу."""

    # Останавливаем слайдшоу
    await state.update_data(playing=False)

    # Ожидаем небольшую задержку, чтобы убедиться, что фоновые задачи завершились
    await asyncio.sleep(0.5)

    try:
        # Удаляем сообщение, если оно ещё существует
        if callback.message:
            await callback.message.delete()
    except TelegramBadRequest:
        await callback.answer("Сообщение уже удалено или не найдено.")

    # Полностью очищаем состояние
    await state.clear()
