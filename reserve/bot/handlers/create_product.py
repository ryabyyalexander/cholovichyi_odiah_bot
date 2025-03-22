from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, InputMediaVideo

from data import del_msg, bot, btn
from data.lexicon import cat
from filters import IsAdmin
from keyboards.ikb import simple_ikb
from sql import data_media
from sql.create_product import data_product
from states.states import State_add_photo

router = Router()


@router.message(((F.text == '+') | (F.text == 'П') | (F.text == 'G')), IsAdmin)
async def start_loader(message: Message, state: FSMContext):
    await state.set_state(State_add_photo.start)
    set_photo: list = []
    await state.update_data(set_photo=set_photo)
    await message.delete()
    text = 'Загрузите фото'
    await message.answer_photo(photo=FSInputFile('download/men.png'),
                               caption=text,
                               reply_markup=simple_ikb(1, 'всі фото ➜ 1 новий товар',
                                                       'кожне фото ➜ 1 новий товар',
                                                       'тільки зберегти фото', btn['x']))


@router.callback_query(F.data.in_(['всі фото ➜ 1 новий товар',
                                   'кожне фото ➜ 1 новий товар',
                                   'тільки зберегти фото']), StateFilter(State_add_photo.start))
async def callback_(callback: CallbackQuery, state: FSMContext):
    product_id = (data_product.get_last_product_id() + 1)
    data = await state.get_data()
    set_photo = data['set_photo']
    if len(set_photo) == 0:
        await callback.answer()
        msg = await callback.message.answer('Загрузите фото')
        await del_msg(msg, 2)
    else:
        if callback.data == 'всі фото ➜ 1 новий товар':
            path = set_photo[0][-2]
            caption = f'product_id ={product_id}\nmain photo\ncaption: {set_photo[0][-1]}'
            type_media = set_photo[0][0]
            if type_media == 'photo':
                media = InputMediaPhoto(media=path, caption=caption)
            else:
                media = InputMediaVideo(media=path, caption=caption)

            await bot.edit_message_media(media=media, chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         reply_markup=simple_ikb(1, btn['x']))
            await callback.answer()

            [photo.insert(0, product_id) for photo in set_photo]
            [data_media.sql_add_photo(data) for data in set_photo]
            data_product.create_products(product_id)

        elif callback.data == 'тільки зберегти фото':
            print('тільки зберегти фото')
            path = set_photo[0][-2]
            caption = f'product_id ={product_id}\nmain photo\ncaption: {set_photo[0][-1]}'
            type_media = set_photo[0][0]
            if type_media == 'photo':
                media = InputMediaPhoto(media=path, caption=caption)
            else:
                media = InputMediaVideo(media=path, caption=caption)
            await bot.edit_message_media(media=media, chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         reply_markup=simple_ikb(1, btn['x']))
            await callback.answer()

            [photo.insert(0, product_id) for photo in set_photo]
            [data_media.sql_add_photo(data) for data in set_photo]
            # data_product.create_products(product_id)
        elif callback.data == 'кожне фото ➜ 1 новий товар':
            for i, data in enumerate(set_photo):
                data.insert(0, product_id)
                data_media.sql_add_photo(data)
                data_product.create_products(product_id)
                product_id += 1
            path = set_photo[0][-2]
            caption = f'product_id ={product_id}\nmain photo\ncaption: {set_photo[0][-1]}'
            type_media = set_photo[0][1]
            if type_media == 'photo':
                media = InputMediaPhoto(media=path, caption=caption)
            else:
                media = InputMediaVideo(media=path, caption=caption)

            await bot.edit_message_media(media=media, chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         reply_markup=simple_ikb(1, btn['x']))
            await callback.answer()
