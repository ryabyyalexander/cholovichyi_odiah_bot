from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from data import btn, del_msg, bot
from data.functions import to_stage, start_info, data_time, get_usd_exchange_rate
from data.lexicon import lennon
from keyboards.ikb import simple_ikb
from sql import data_media, data_product
from states.states import State_album, State_add_photo

router = Router()


@router.callback_query(F.data.in_([btn['x'], btn['close']]))
async def process_sl(callback: CallbackQuery, state: FSMContext):
    state_now = await state.get_state()

    formatted_date = data_time()
    usd_rate = get_usd_exchange_rate()
    if state_now == State_add_photo.start:
        await callback.message.delete()

    if callback.data == btn['close']:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
        await state.clear()



    if state_now == State_album.favorites:
        data = await state.get_data()
        more_info = False
        await to_stage(data['photos'], callback, state, more_info=more_info,
                       filters=data['filters'])
        await state.set_state(State_album.start)
        await state.update_data(more_info=more_info, album_on=False)
        await state.set_state(State_album.start)
        await callback.answer()
    else:
        cap = "\n".join(start_info())
        caption = f"""
<b>Чоловічий одяг\nМонмартр 158   🏃🏻‍♂️🚶🏻👫  ️🚶🏻</b>
"""
        # video = data_media.sql_get_video(2, 'video')
        try:
            await bot.edit_message_media(
                media=InputMediaPhoto(media=lennon, caption=caption),
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=simple_ikb(2,
                                        '➔       новинки', '✖️ закрити', filters=True))
        except TelegramBadRequest:
            pass


@router.callback_query(F.data.in_(['➔       новинки', '➔      новинки']))
async def process_sl(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State_album.start)

    # получаем все главные фото из базы данных
    photos = data_media.sql_get_main_prod_photo()

    # проверяет, является ли фото продуктом, если да, то остаётся в обновлённом списке
    photos = [photo for photo in photos if data_product.photo_is_product(photo[0])]

    # выполняем функцию "НА СЦЕНУ"
    await to_stage(photos, callback, state, shaffle=True, more_info=True, filters=True)

    if callback.data == '➔      новинки':
        await callback.message.delete()


@router.callback_query(F.data.in_(['new']))
async def process_sl(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State_album.start)

    # получаем все главные фото из базы данных
    photos = data_media.sql_get_new_photo()

    # проверяет, является ли фото продуктом, если да, то остаётся в обновлённом списке
    photos = [photo for photo in photos if data_product.photo_is_product(photo[0])]

    # выполняем функцию "НА СЦЕНУ"
    await to_stage(photos, callback, state, shaffle=True, more_info=True)

    if callback.data == '➔      новинки':
        await callback.message.delete()


@router.callback_query(F.data.in_([btn['>'], btn['<']]))
async def process_navigation(callback: CallbackQuery, state: FSMContext):
    state_now = await state.get_state()
    data = await state.get_data()

    if state_now == State_album.favorites:
        photos = data['favorites']
        album_on = True
        is_favorite_photos = True
        new_captions = f"Збережене   ★    ({len(photos)})\n"

    elif state_now == State_album.size:
        photos = data['photos']
        new_captions = ''
        album_on = False
        is_favorite_photos = False

    else:
        photos = data['photos']
        album_on = False
        is_favorite_photos = False
        new_captions = ''

    more_info = data['more_info']
    filters = data['filters']

    if len(photos) > 1:
        if callback.data == btn['>']:
            photos.append(photos.pop(0))
        elif callback.data == btn['<']:
            photos.insert(0, photos.pop())
        await state.update_data(favorites=photos)

        await to_stage(photos, callback, state,
                       album_on=album_on,
                       is_favorite_photos=is_favorite_photos,
                       more_info=more_info, filters=filters, new_captions=new_captions)
    else:
        msg = await callback.message.answer('Тільки один продукт')
        await callback.answer()
        await del_msg(msg, 2)


@router.callback_query(F.data.in_([btn['star_cl'], btn['star_fl']]), StateFilter(State_album.start))
async def process_star_toggle(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    kb_size = False
    photos = data['photos']
    user_id = callback.from_user.id
    is_starred = callback.data == btn['star_cl']
    more_info = data['more_info']
    filters = data['filters']

    if is_starred:
        data_media.sql_add_favorite(photos[0], user_id)
        await callback.answer()
    else:
        data_media.sql_delete_favorite(photos[0][-2], user_id)
        await callback.answer()

    await to_stage(photos, callback, state, more_info=more_info, filters=filters, kb_size=kb_size)


@router.callback_query(F.data == btn['favorite_off'])
async def show_favorites(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State_album.start)
    user_id = callback.from_user.id
    more_info = True
    favorites = data_media.sql_get_favorites(user_id)
    await state.update_data(album_on=True)
    await to_stage(favorites, callback, state, album_on=True, is_favorite_photos=True,
                   more_info=more_info, new_captions=f"Збережене   ★    ({len(favorites)})\n")
    await state.set_state(State_album.favorites)
    await callback.answer()


@router.callback_query(F.data == btn['star_fl'], StateFilter(State_album.favorites))
async def toggle_star_favorites(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    favorites = data['favorites']
    filters = data['filters']
    data_media.sql_delete_favorite(favorites[0][-2], user_id)
    favorites.pop(0)
    await state.update_data(favorites=favorites)

    if favorites:
        await to_stage(favorites, callback, state, album_on=True, is_favorite_photos=True,
                       more_info=True, filters=filters,
                       new_captions=f'Ви відзначили ★    ({len(favorites)})\n')
        await callback.answer()

    else:
        photos = data['photos']
        await to_stage(photos, callback, state, album_on=False, more_info=True)
        await state.set_state(State_album.start)
        # msg = await callback.message.answer('Ваш блокнот пуст')
        # await del_msg(msg, 3)
    await callback.answer()


@router.callback_query(F.data.in_([btn['+']]))
async def add_admin_buttons(callback: CallbackQuery, state: FSMContext):
    await state.update_data(more_info=True)
    data = await state.get_data()
    state_now = await state.get_state()
    if state_now == State_album.favorites:
        await to_stage(data['favorites'], callback, state, is_favorite_photos=True, album_on=True,
                       more_info=data['more_info'])
    else:
        await to_stage(data['photos'], callback, state, more_info=data['more_info'])

    await callback.answer()


@router.callback_query(F.data.in_([btn['-']]))
async def remove_admin_buttons(callback: CallbackQuery, state: FSMContext):
    await state.update_data(more_info=False, filters=False)
    data = await state.get_data()
    # for key, value in data.items():
    #     print(f"Ключ: {key}, Значение: {value}")
    await to_stage(data['photos'], callback, state, more_info=data['more_info'], filters=data['filters'])
    await callback.answer()


@router.callback_query(F.data.in_([btn['<<'], btn['>>']]))
async def next_buttons(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    kb_size = False
    product_photos = data['product_photos']
    more_info = data['more_info']
    album_on = data['album_on']
    filters = data['filters']
    set_photo = [list(i) for i in product_photos]
    if len(set_photo) > 1:
        if callback.data == btn['>>']:
            set_photo.append(set_photo.pop(0))
        elif callback.data == btn['<<']:
            set_photo.insert(0, set_photo.pop())

        await to_stage(set_photo, callback, state, is_product_photos=True, album_on=album_on, more_info=more_info,
                       filters=filters, kb_size=kb_size)
        await callback.answer()
        await state.update_data(product_photos=set_photo, filters=filters)
    else:
        msg = await callback.message.answer(f"В альбомі тільки одне фото")
        await del_msg(msg, 3)
    await callback.answer()


@router.callback_query(F.data == btn['filters'])
async def open_filters(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photos = data['photos']
    await state.update_data(filters=True)
    await to_stage(photos, callback, state, more_info=True, filters=True)
    await callback.answer()


@router.callback_query(F.data.in_([btn['close_filters']]))
async def remove_admin_buttons(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await to_stage(data['photos'], callback, state, more_info=True)
    await state.update_data(filters=False)
    await callback.answer()


@router.callback_query(F.data == '.')
async def remove_dot(callback: CallbackQuery):
    await callback.answer()
