from aiogram.fsm.state import (
    State,
    StatesGroup
)


class Registration(StatesGroup):
    child_name = State()