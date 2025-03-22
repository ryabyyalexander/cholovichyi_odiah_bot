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


async def display_media(photos: list,
                        callback: CallbackQuery,
                        state: FSMContext,
                        shuffle: bool = False,
                        is_favorite: bool = False,
                        more_info: bool = False,
                        filters: bool = False,
                        current_kb: bool = False,
                        new_caption: str = '') -> None:
    """Отображает фото или видео с информацией о товаре."""

    # Перемешиваем фото, если требуется
    if shuffle:
        random.shuffle(photos)

    # Получаем данные о текущем состоянии
    state_now = await state.get_state()
    user_id = callback.from_user.id
    favorites = data_media.sql_get_favorites(user_id)

    # Проверяем, добавлено ли фото в избранное
    is_starred = photos[0] in favorites
    favorites_are = bool(favorites)

    # Получаем информацию о товаре
    product_photos = data_media.sql_get_photo_prod_id(photos[0][0])
    product_id = photos[0][0]
    name = data_product.get_param_product(product_id, 'name')
    price = data_product.get_param_product(product_id, 'cena')
    category = data_product.get_param_product(product_id, 'category')
    brand = data_product.get_param_product(product_id, 'brand')
    seasons = data_product.get_param_product(product_id, 'seasons')
    euro_rate = get_euro_exchange_rate()

    # Получаем доступные размеры для товара
    all_sizes = [data_product.get_sizes_product(i[0]) for i in photos]
    available_sizes = get_available_sizes(category, all_sizes)

    # Генерируем заголовок для медиафайла
    caption = generate_caption(new_caption, photos, category, brand, name, seasons, price, euro_rate, available_sizes)

    # Выбираем тип медиафайла (фото или видео)
    media = get_media_class(photos[0], caption)

    # Определяем клавиатуру
    kb = callback.message.reply_markup if current_kb else ikb(
        is_starred, favorites_are, more_info=more_info, filters=filters, user_id=user_id)

    # Обновляем сообщение с медиафайлом
    await bot.edit_message_media(
        media=media,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=kb
    )

    # Обновляем состояние FSM
    await state.update_data(favorites_are=favorites_are, product_photos=product_photos, product_id=product_id)
    await callback.answer()


def get_available_sizes(category: str, all_sizes: list) -> list:
    """Возвращает доступные размеры для категории товара."""
    size_template = {
        'куртки': ["32", "33", "34", "35", "36", "38", "40", "42", "46", "48", "50", "52", "54", "56", "58", "60"],
        'штаны': ["xs", "s", "m", "l", "xl", "2xl", "3xl", "4xl"]
    }.get(category, [])

    return [size for i, size in enumerate(size_template) if all_sizes[0][i] != 0]


def generate_caption(new_caption: str, photos: list, category: str, brand: str, name: str,
                     seasons: str, price: float, euro_rate: float, sizes: list) -> str:
    """Генерирует описание товара для подписи к фото."""
    return f'''
{new_caption}{photos[0][-1]}
<code>{category} • {brand}\n{seasons}  {name}</code>
<code>{"ціна: "}</code><b>{price} €   {round(price * euro_rate)} UAH</b>
<code>{"розм. " if sizes else ""}</code><b>{"  ".join(sizes)}</b>'''


def get_media_class(photo_info: list, caption: str):
    """Возвращает класс медиафайла в зависимости от его типа."""
    media_classes = {
        'photo': InputMediaPhoto,
        'video': InputMediaVideo
    }
    media_type = photo_info[1]
    media_class = media_classes.get(media_type)

    return media_class(media=photo_info[-2], caption=caption)


def get_euro_exchange_rate() -> float:
    """Получает текущий курс евро с сайта НБУ."""
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data[0]['rate']
    raise Exception("Не удалось получить данные с сайта НБУ")


async def del_msg(message: Message, delay: int) -> None:
    """Удаляет сообщение через заданное время."""
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except TelegramBadRequest:
        pass
