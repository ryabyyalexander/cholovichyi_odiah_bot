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


@router.message(F.text == '/start')
async def process_start_command(message: Message, state: FSMContext):
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

    # else:
    #     await message.answer(text = f'{rest[0]}'
    #     )

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


@router.message(F.text.lower().in_(['==']))
async def process_total_command(message: Message, state: FSMContext):
    await message.delete()
    formatted_date = data_time()
    all_results = data_product.get_total_products()[1:]  # Получаем все товары (без заголовка)

    # Разбиваем на страницы по 50 товаров
    page_size = 50
    pages = [all_results[i:i + page_size] for i in range(0, len(all_results), page_size)]
    total_pages = len(pages)

    # Сохраняем данные в state для навигации
    await state.update_data(
        current_page=0,
        total_pages=total_pages,
        pages=pages,
        formatted_date=formatted_date
    )

    # Отправляем первую страницу
    await show_products_page(message, state)


async def show_products_page(message: Message, state: FSMContext):
    data = await state.get_data()
    current_page = data['current_page']
    total_pages = data['total_pages']
    pages = data['pages']
    formatted_date = data['formatted_date']

    # Формируем сообщение для текущей страницы
    output = []
    for row in pages[current_page]:
        if row[0] == 'ИТОГО':
            # Итоги добавляем только на последней странице
            if current_page == total_pages - 1:
                output.append(f"{row[0]}\t\t\t{row[4]}\nКоличество единиц: {row[2]}\n{formatted_date}")
        else:
            name = row[1].split('\n')[0]  # Берем только название товара
            output.append(f"{row[0]} - {name}\t - {row[2]}\t * {row[3]}\t = {row[4]}")

    # Добавляем номер страницы (если страниц несколько)
    if total_pages > 1:
        output.append(f"\nСтраница {current_page + 1}/{total_pages}")

    # Создаем клавиатуру
    keyboard = []
    if total_pages > 1:
        if current_page > 0:
            keyboard.append(InlineKeyboardButton(text="Назад", callback_data="prev_page"))
        if current_page < total_pages - 1:
            keyboard.append(InlineKeyboardButton(text="Вперед", callback_data="next_page"))

    keyboard.append(InlineKeyboardButton(text="✖️ Закрыть", callback_data="close_pages"))
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[keyboard])

    # Отправляем или редактируем сообщение
    if 'message_id' in data:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data['message_id'],
                text="\n".join(output),
                reply_markup=reply_markup
            )
            return
        except TelegramBadRequest:
            pass

    msg = await message.answer("\n".join(output), reply_markup=reply_markup)
    await state.update_data(message_id=msg.message_id)


@router.callback_query(F.data.in_(["prev_page", "next_page", "close_pages"]))
async def handle_page_navigation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "close_pages":
        await callback.message.delete()
        await state.clear()
        return

    current_page = data['current_page']

    if callback.data == "prev_page" and current_page > 0:
        await state.update_data(current_page=current_page - 1)
    elif callback.data == "next_page" and current_page < data['total_pages'] - 1:
        await state.update_data(current_page=current_page + 1)

    await show_products_page(callback.message, state)
    await callback.answer()


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
