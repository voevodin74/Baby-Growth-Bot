from aiogram import Router

from aiogram.filters import (
    CommandStart
)

from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)

from aiogram.fsm.context import (
    FSMContext
)

from storage import (
    user_exists
)

from calendar_widget import (
    create_calendar
)

from keyboards import (
    MAIN_MENU
)

from states import (
    Registration
)

router = Router()


@router.message(
    CommandStart()
)
async def start(
        message: Message,
        state: FSMContext
):

    if user_exists(
            message.from_user.id
    ):

        await message.answer(
            "👶 Ребенок уже зарегистрирован",
            reply_markup=MAIN_MENU
        )

        return

    await message.answer(
        "Привет 👋\n\n"
        "Как зовут ребенка?",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        Registration.child_name
    )


@router.message(
    Registration.child_name
)
async def child_name(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        child_name=message.text
    )

    await message.answer(
        "📅 Выберите дату рождения:",
        reply_markup=create_calendar()
    )