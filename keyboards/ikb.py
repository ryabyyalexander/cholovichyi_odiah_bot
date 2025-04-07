from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import btn
from data.lexicon import CATEGORY, SIZE


# В файле ikb.py изменить функцию ikb():
def ikb(is_starred: bool = False,
        favorites_are: bool = False,
        more_info: bool = False,
        album_on: bool = False,
        filters: bool = False,
        kb_size: bool = False,
        size_list=None,
        user_id=None,
        link=None,
        has_multiple_photos: bool = False) -> InlineKeyboardMarkup:  # Добавляем новый параметр
    if size_list is None:
        size_list = []
    kb_builder = InlineKeyboardBuilder()

    btn_filters = btn['filters'] if not filters else btn['close_filters']
    buttons = [btn['<'], btn['>']]

    if link:
        kb_builder.row(InlineKeyboardButton(text="Детальніше", url=link))

    first_line_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in buttons]
    kb_builder.row(*first_line_btn, width=6)

    # Изменяем эту часть кода:
    buttons = [btn_filters]
    if has_multiple_photos:  # Добавляем кнопки только если есть несколько фото
        buttons.extend([btn['<<'], btn['>>']])
    buttons.append(btn['x'])

    album_on and buttons.pop(0)

    more_info_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in buttons]
    kb_builder.row(*more_info_btn, width=4)

    # Остальной код остается без изменений
    if kb_size:
        size_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in size_list]
        kb_builder.row(*size_btn, width=8)

    if filters:
        cat_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in CATEGORY]
        kb_builder.row(*cat_btn, width=3)

    return kb_builder.as_markup()


def simple_ikb(width: int,
               *args: str,
               filters=False,
               kb_size=False,
               btn_close: bool = False,
               **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    kb_builder.row(*buttons, width=width)

    if filters:
        cat_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in CATEGORY]
        kb_builder.row(*cat_btn, width=3)
    if btn_close:
        kb_builder.row(InlineKeyboardButton(text=btn['close'], callback_data=btn['close']), width=1)
    if kb_size:
        size_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in SIZE]
        kb_builder.row(*size_btn, width=8)

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
