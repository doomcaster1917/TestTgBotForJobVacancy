from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

class MenuForm(StatesGroup):
    action_type_choosen = State()
    media_data_downloaded = State()
    text_received = State()
