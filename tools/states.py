from aiogram.dispatcher.filters.state import State, StatesGroup

class User_state(StatesGroup):
    menu = State()
    game = State()
