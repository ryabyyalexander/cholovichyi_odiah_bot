import asyncio
import random
from datetime import datetime
import requests
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, CallbackQuery
from data import bot, btn
from data.lexicon import CATEGORY, city25club
from keyboards import ikb
from sql import data_media, data_product
from states.states import State_album


async def to_stage(photos: list,
                   callback: CallbackQuery | None = None,
                   state: FSMContext | None = None,
                   shaffle=False,
                   is_favorite_photos=False,
                   is_product_photos=False,
                   is_size_photos=False,
                   album_on=False,
                   more_info=False,
                   current_kb=False,
                   filters=False,
                   kb_size=False,
                   new_captions=''):
    if shaffle:
        random.shuffle(photos)
    # print(f'************************************************************to_stage is run\n')
    # print(f'{len(photos)} photos = {photos}')

    state_now = await state.get_state()
    # print(f'state: {state_now}')
    # print(f'callback: {callback.data}')

    user_id = callback.from_user.id
    favorites = data_media.sql_get_favorites(user_id)
    is_starred = photos[0] in favorites
    favorites_are = True if favorites else False

    #     print(f"""
    # user_id = {user_id}
    # favorites = {favorites}
    # is_starred = {is_starred}
    # favorites_are ={favorites_are}""")

    product_photos = data_media.sql_get_photo_prod_id(photos[0][0])
    product_id = photos[0][0]

    #     print(f"""
    # product_photos = {product_photos}
    # product_id = {product_id}""")

    name: str = data_product.get_param_product(product_id, 'name')
    cena = data_product.get_param_product(product_id, 'cena')
    price = data_product.get_param_product(product_id, 'price')

    category = data_product.get_param_product(product_id, 'category')
    brand = data_product.get_param_product(product_id, 'brand')
    seasons = data_product.get_param_product(product_id, 'seasons')

    link =  data_product.get_param_product(product_id, 'article')

    if link == '0':
        link=None

    euro_rate = get_euro_exchange_rate()
    usd_rate = get_usd_exchange_rate()

    #     print(f"""
    # name = {name},
    # cena = {cena},
    # category = {category},
    # brand = {brand}
    # """)

    all_size = [data_product.get_sizes_product(i[0]) for i in photos]
    # print(f'all_size: {all_size}')
    # all_product_id = [i[0] for i in photos]
    # quant_all_size = sum([sum(data_product.get_sizes_product(i[0])) for i in photos])
    # quant_size_prod_id = sum(size)
    if category in ['куртки', 'джинси', 'шорти']:
        shablon = ["32", "33", "34", "35", "36", "38", "40", "42",
                   "46", "48", "50", "52", "54", "56", "58", "60"]
    else:
        shablon = ["32", "33", "34", "35", "36", "38", "40", "42",
                   "xs", "s", "m", "l", "xl", "2xl", "3xl", "4xl"]

    size = [(shablon[i]) for i in range(len(shablon)) if all_size[0][i] != 0]
    size_list = []

    # print(f'size: {size}')
    # print(f'size_list = {size_list}')

    if filters:
        list_category_size = [[shablon[i] for i in range(len(shablon)) if all_size[j][i] != 0] for j in
                              range(len(photos))]

        await state.update_data(list_category_size=list_category_size)

        set_size = set()
        for i in list_category_size:
            for j in i:
                set_size.add(j)

        sorted_list_size = sorted(list(set_size))
        # print(f'sorted_list_size: {sorted_list_size}')

        if size[0] in ["32", "33", "34", "35", "36", "38", "40", "42"]:
            for i in ["32", "33", "34", "35", "36", "38", "40", "42"]:
                if i in sorted_list_size:
                    size_list.append(i)
                else:
                    size_list.append('-')

        elif size[0] in ["46", "48", "50", "52", "54", "56", "58", "60"]:
            for i in ["46", "48", "50", "52", "54", "56", "58", "60"]:
                if i in sorted_list_size:
                    size_list.append(i)
                else:
                    size_list.append('-')

        elif size[0] in ["xs", "s", "m", "l", "xl", "2xl", "3xl", "4xl"]:
            for i in ["xs", "s", "m", "l", "xl", "2xl", "3xl", "4xl"]:
                if i in sorted_list_size:
                    size_list.append(i)
                else:
                    size_list.append('-')

        # print(f'size_list = {size_list}')

    # caption = f'{new_captions}{photos[0][-1]}\n\n<code>{category} • {brand}\n{name}</code>\n\n' \
    #           f'<b>{cena} €   {round(cena * euro_rate)} UAH</b>\n\n<code><b>{" | ".join(size)}</b></code>'

    caption = f'''
{new_captions}{photos[0][-1]}
<code>{category} • {brand}\n{seasons}  {name}</code>
<code>{"ціна: "}</code><b>{round(price * usd_rate)} гривень - {price}💲</b>
<code>{"розм. " if len(size) != 0 else ""}</code><b>{"  ".join(size)}</b>'''

    # print(caption, end='\n')

    if len(size_list) != 0:
        size = size_list

    if current_kb:
        kb = callback.message.reply_markup
    else:
        kb = ikb(is_starred, favorites_are,
                 album_on=album_on, more_info=more_info,
                 filters=filters, kb_size=kb_size, size_list=size,
                 user_id=user_id, link=link)

    type_media = photos[0][1]

    media_classes = {
        'photo': InputMediaPhoto,
        'video': InputMediaVideo
    }

    media_class = media_classes.get(type_media)
    if callback.data == '➔      новинки':
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photos[0][-2],
                             caption=caption,
                             parse_mode="HTML",
                             reply_markup=ikb(is_starred, favorites_are, more_info=more_info, filters=filters, link=link)
                             )
    else:
        if callback.data == btn['x']:
            media = InputMediaPhoto(media=city25club, caption=caption)
            if state_now == State_album.favorites:
                media = media_class(media=photos[0][-2], caption=caption)
        else:
            media = media_class(media=photos[0][-2], caption=caption)
        if media_class:
            await bot.edit_message_media(
                media=media,
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=kb)

    await state.update_data(favorites_are=favorites_are,
                            album_on=album_on,
                            is_starred=is_starred,
                            more_info=more_info,
                            filters=filters)

    if is_favorite_photos:
        await state.update_data(favorites=photos, product_photos=product_photos, product_id=product_id)

    elif is_product_photos:
        await state.update_data(product_photos=product_photos)

    elif is_size_photos:
        await state.update_data(size_photos=photos)

    else:
        await state.update_data(photos=photos, product_photos=product_photos, product_id=product_id)

    # data = await state.get_data()
    # print('\nв памяти состояния:\n')
    # [print(i, data[i]) for i in data]
    await callback.answer()


# async def create_kb(callback: CallbackQuery,
#                     is_starred=False,
#                     favorites_are=False,
#                     album_on=False,
#                     more_info=False,
#                     filters=False,
#                     kb_size=False,
#                     size_list=False,
#                     current_kb=False):
#     if current_kb:
#         kb = callback.message.reply_markup
#         return kb
#     else:
#         kb = ikb(is_starred, favorites_are,
#                  album_on=album_on, more_info=more_info, filters=filters, kb_size=kb_size, size_list=size_list,
#                  user_id=callback.from_user.id)
#
#         return kb


async def del_msg(message: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except TelegramBadRequest:
        pass


# Словари для названий месяцев и дней недели
months = {
    1: "січня", 2: "лютого", 3: "березня", 4: "квітня",
    5: "травня", 6: "червня", 7: "липня", 8: "серпня",
    9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня"
}

days_of_week = {
    0: "понеділок", 1: "вівторок", 2: "середа",
    3: "четвер", 4: "п’ятниця", 5: "субота", 6: "неділя"
}


# Получение текущей даты


def data_time():
    now = datetime.now()
    # Форматирование даты
    day = now.day
    month = months[now.month]
    day_of_week = days_of_week[now.weekday()]
    year = now.year

    return f"{day} {month} {year}, {day_of_week}"


def get_euro_exchange_rate():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Не удалось получить данные с сайта НБУ")

    data = response.json()

    if not data or 'rate' not in data[0]:
        raise Exception("Не удалось найти курс евро")

    return data[0]['rate']

def get_usd_exchange_rate():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Не удалось получить данные с сайта НБУ")

    data = response.json()

    if not data or 'rate' not in data[0]:
        raise Exception("Не удалось найти курс доллара")

    return data[0]['rate']


def start_info():
    list_cat = []
    for category in CATEGORY:
        category_product = data_product.get_category_product(category)
        list_product_id_from_category_product = [prod[0] for prod in category_product]
        n_models = len(list_product_id_from_category_product)
        list_quant = [sum(data_product.get_sizes_product(product_id=i)) for i in list_product_id_from_category_product]
        quantity_in_category = sum(list_quant)

        list_cat.append(f'<code>{category}: {n_models} мод.</code>')
    return list_cat

# list_cat.append(f'<code>{category}: {n_models} мод. {quantity_in_category} шт.</code>')
