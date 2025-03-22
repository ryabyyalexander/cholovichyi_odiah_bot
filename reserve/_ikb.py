from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import btn, admins
from data.lexicon import CATEGORY, SIZE, RED


def ikb(is_starred: bool = False,
        favorites_are: bool = False,
        more_info: bool = False,
        album_on: bool = False,
        filters: bool = False,
        kb_size: bool = False,
        size_list=None,
        user_id=None) -> InlineKeyboardMarkup:
    if size_list is None:
        size_list = []
    kb_builder = InlineKeyboardBuilder()

    star = btn[f'star_{"fl" if is_starred else "cl"}']
    favorite_button = btn['album'] if album_on else btn['favorite_off']
    plus = btn['-'] if more_info else btn['+']
    buttons = [btn['x'], star, plus, btn['<'], btn['>']]
    album_on and buttons.pop(-3)

    first_line_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in buttons]
    kb_builder.row(*first_line_btn, width=6)

    if more_info:
        btn_filters = btn['filters'] if not filters else btn['close_filters']
        buttons = [btn_filters, btn['<<'], btn['>>']] if not album_on else [btn['<<'], btn['>>']]
        favorites_are and buttons.insert(0, favorite_button)
        more_info_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in buttons]
        kb_builder.row(*more_info_btn, width=4)

    if kb_size:
        size_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in size_list]
        kb_builder.row(*size_btn, width=8)

    if filters:
        cat_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in CATEGORY]
        kb_builder.row(*cat_btn, width=3)

    # if user_id in admins:
    #     cat_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in RED]
    #     kb_builder.row(*cat_btn, width=6)

    return kb_builder.as_markup()


def simple_ikb(width: int,
               *args: str,
               filters=False,
               kb_size=False,
               btn_close: bool = False,
               **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
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

    if filters:
        cat_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in CATEGORY]
        kb_builder.row(*cat_btn, width=3)
    if btn_close:
        kb_builder.row(InlineKeyboardButton(text=btn['close'], callback_data=btn['close']), width=1)
    if kb_size:
        size_btn = [InlineKeyboardButton(text=button, callback_data=button) for button in SIZE]
        kb_builder.row(*size_btn, width=8)

    return kb_builder.as_markup()
