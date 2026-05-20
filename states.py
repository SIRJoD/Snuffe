from aiogram.fsm.state import State, StatesGroup


class SellForm(StatesGroup):
    waiting_for_details = State()
    waiting_for_confirmation = State()