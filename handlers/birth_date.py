from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message
)

from aiogram.fsm.context import (
    FSMContext
)

from storage import (
    load_user
)

from calendar_widget import (
    create_calendar
)

router = Router()


@router.message(
    F.text == "🔄 Изменить дату рождения"
)
async def change_birth_date(
        message: Message,
        state: FSMContext
):

    user = load_user(
        message.from_user.id
    )

    if not user:
        return

    #
    # Сохраняем имя ребенка
    # чтобы calendar.py смог
    # пересоздать события
    #
    await state.update_data(
        child_name=user[
            "child_name"
        ]
    )

    await message.answer(
        "📅 Выберите новую дату рождения:",
        reply_markup=create_calendar()
    )