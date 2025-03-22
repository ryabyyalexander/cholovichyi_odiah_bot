from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

# from data import del_msg
from data.lexicon import CATEGORY, SIZE, size_jeans, size_letter
from handlers.photo_gallery import to_stage
from sql import data_product, data_media
from states.states import State_album

router = Router()


@router.callback_query(F.data.in_(CATEGORY))
async def cat(callback: CallbackQuery, state: FSMContext):
    await state.set_state(State_album.start)
    if await state.get_state() is not None:
        category_product = data_product.get_category_product(callback.data)
        list_product_id_from_category_product = [prod[0] for prod in category_product]
        n_models = len(list_product_id_from_category_product)
# list_quant = [sum(data_product.get_sizes_product(product_id=i)) for i in list_product_id_from_category_product]
# quantity_in_category = sum(list_quant)

        photos = [data_media.sql_get_main_prod_photo(product_id=i)[0] for i in list_product_id_from_category_product]
        cap = 'знайшлась' if n_models == 1 else 'знайшлось'
        await to_stage(photos, callback, state,
                       shaffle=True, more_info=True,
                       filters=True, kb_size=True,
                   new_captions=f'''
<b>{callback.data}</b>
{cap}  ➜  {n_models} мод.
''')
#         msg = await callback.message.answer(f'''
# <b>{callback.data}</b>
# {cap}  ➜  {n_models} мод.
# ''')
        await state.update_data(kb_size=True)
        # await del_msg(msg, 3)


@router.callback_query(F.data.in_(list(SIZE+size_jeans+size_letter)))
async def cat(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    kb_size = False
    await state.update_data(kb_size=kb_size)

    list_category_size = data['list_category_size']
    photos = data['photos']

    new_list_size = []
    for i, photo in enumerate(photos):
        if callback.data in list_category_size[i]:
            new_list_size.append(photo)

    cap = 'знайшлась' if len(new_list_size) == 1 else 'знайшлось'
    await state.update_data(new_list_size=new_list_size)
    await to_stage(new_list_size, callback, state,
                   more_info=True, filters=False, kb_size=kb_size,
                   new_captions=f"""
У розмірі  <b>{callback.data}</b>
{cap}:  <b>{len(new_list_size)}</b>  мод.
""")

#     msg = await callback.message.answer(f"""
# У розмірі  <b>{callback.data}</b>
# {cap}:  <b>{len(new_list_size)}</b>  мод.
# """)
#     await del_msg(msg, 3)
