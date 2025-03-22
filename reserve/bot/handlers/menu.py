from aiogram import Router, F
from aiogram.types import Message

from data import btn, menu_user, menu_admin, admin
from keyboards import ikb

router = Router()


@router.message(F.text == '/menu')
async def process_press_menu(message: Message):
    await message.delete()
    if message.from_user.id == admin:
        await message.answer(menu_admin, reply_markup=ikb(1, btn['x']))
    else:
        await message.answer(menu_user, reply_markup=ikb(1, btn['x']))
