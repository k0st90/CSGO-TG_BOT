from aiogram.fsm.state import StatesGroup, State

class Nickname(StatesGroup):
    get_player = State()
    update_player = State()