import asyncio
from random import shuffle

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F
from data import admins, bot, btn
from data.functions import start_info, data_time, get_euro_exchange_rate
from data.lexicon import cat
from filters import IsAdmin
from keyboards.ikb import simple_ikb
from sql import data_users, data_media, data_product
from states.states import State_album

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
    euro_rate = get_euro_exchange_rate()
    rest = ['🚶🏻👫🚶🏻👫🚶🏻👫🏃🏻🕺🏻🚶‍♂️🚶‍♀️',
            '🏃🏻‍♂️🧍🏻🧍‍♀️🧍🏻🧍🏽‍♂️👫👭👬🧍🏽‍♂️🧍‍♀️🧍🏻',
            '🏃🏻‍👫',
            '🏃🏻‍🏃🏼‍♂👫👭👬🧍🧍🏼‍♂️🏃🏻‍♀️',
            '🚶🏻👫🏃🏻‍♂️🚶🏻👫🚶🏻👫🚶🏻🚘🚖👫',
            '🕺🏻',
            '👭👬️',
            '👫👫🚶🏻🏃🏻']

    shuffle(rest)
    if restart_count < 1:
        await message.answer(text="""

🚶🏻👫    🏃🏻‍♂️🚶🏻   🚘🚖  👫🚶🏻👫
М⭕️ДНИЙ ШОПІНГ В  ОДЕСІ""")

    else:
        pass
        # await message.answer(rest[0])

    # выполняем первый СТАРТ - запуск ИНТРО
    if restart_count < 100000:
        data_users.update_restart_count(user_id)
        try:
            video = data_media.sql_get_video(1, 'video')
            captions = video[0][1].split('\r\n\r\n')
            video = video[0][0]
            current_caption = captions[0]

            msg = await message.answer_video(video=video,
                                             caption=f'''
                                             
{current_caption}

<code>{formatted_date}
в наявності:</code>

{caption_start_info}

<b>1 евро - {round(euro_rate, 2)} UAH</b>   <i>(з сайту НБУ)</i>
''', reply_markup=simple_ikb(2, '➔      новинки'))

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

<b>1 евро - {round(euro_rate, 2)} UAH</b>   <i>(з сайту НБУ)</i>
''', reply_markup=simple_ikb(2, '➔      новинки'))
                except TelegramBadRequest:
                    pass
                    break  # Выход из цикла при ошибке

        except TelegramBadRequest:
            pass
    else:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=cat,
                             caption=f"""
<code>{formatted_date}
в наявності та вчасно:</code>

{caption_start_info}

<b>1 евро - {round(euro_rate, 2)} UAH</b>   <i>(з сайту НБУ)</i>
""",
                             reply_markup=simple_ikb(1, '➔      новинки'))
        await message.delete()

        data_users.update_restart_count(user_id)


@router.message(F.text.lower().in_(['==', 'отчет', 'ооо']))
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