from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

menu = KeyboardButton(text='Просмотреть каталог товаров')

builder.row(menu)
builder.adjust(1)

kb_start: ReplyKeyboardMarkup = builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder=f'enter your size'
)
