from aiogram.fsm.state import State, StatesGroup


class State_album(StatesGroup):
    start = State()
    favorites = State()
    size = State()


class State_load_product(StatesGroup):
    load_photo = State()
    load_content = State()


class State_excursion(StatesGroup):
    start = State()


class State_add_photo(StatesGroup):
    start = State()
    close = State()
