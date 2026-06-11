from aiogram import Router
from aiogram import F

from aiogram.types import (
    CallbackQuery
)

from aiogram.fsm.context import (
    FSMContext
)

from generator import (
    generate_events
)

from storage import (
    save_user,
    load_user
)

from calendar_widget import (
    create_calendar
)

from keyboards import (
    MAIN_MENU
)

from utils import (
    format_date
)

router = Router()


@router.callback_query(
    F.data == "ignore"
)
async def ignore_callback(
        callback: CallbackQuery
):
    await callback.answer()


@router.callback_query(
    F.data.startswith("prev:")
)
async def prev_month(
        callback: CallbackQuery
):

    _, year, month = (
        callback.data.split(":")
    )

    year = int(year)
    month = int(month)

    month -= 1

    if month == 0:

        month = 12
        year -= 1

    await callback.message.edit_reply_markup(
        reply_markup=create_calendar(
            year,
            month
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("next:")
)
async def next_month(
        callback: CallbackQuery
):

    _, year, month = (
        callback.data.split(":")
    )

    year = int(year)
    month = int(month)

    month += 1

    if month == 13:

        month = 1
        year += 1

    await callback.message.edit_reply_markup(
        reply_markup=create_calendar(
            year,
            month
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("day:")
)
async def select_day(
        callback: CallbackQuery,
        state: FSMContext
):

    _, year, month, day = (
        callback.data.split(":")
    )

    birth_date = (
        f"{year}-"
        f"{int(month):02d}-"
        f"{int(day):02d}"
    )

    data = await state.get_data()

    child_name = data.get(
        "child_name"
    )

    #
    # Если меняем дату рождения,
    # имя берем из сохраненного профиля
    #
    if not child_name:

        user = load_user(
            callback.from_user.id
        )

        child_name = (
            user["child_name"]
        )

    events = generate_events(
        birth_date
    )

    save_user(
        {
            "telegram_id":
                callback.from_user.id,

            "child_name":
                child_name,

            "birth_date":
                birth_date,

            "events":
                events
        }
    )

    await state.clear()

    await callback.message.edit_text(
        "✅ Данные сохранены"
    )

    await callback.message.answer(
        f"👶 {child_name}\n\n"
        f"📅 Дата рождения:\n"
        f"{format_date(birth_date)}",
        reply_markup=MAIN_MENU
    )

    await callback.answer()