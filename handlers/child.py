from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message
)

from storage import (
    load_user
)

from utils import (
    format_date
)

router = Router()


@router.message(
    F.text == "👶 Мой ребенок"
)
async def child_info(
        message: Message
):

    user = load_user(
        message.from_user.id
    )

    if not user:

        await message.answer(
            "Сначала выполните /start"
        )

        return

    growth_count = len(
        [
            e for e in user["events"]
            if e.get("type") == "growth"
        ]
    )

    milestone_count = len(
        [
            e for e in user["events"]
            if e.get("type") == "milestone"
        ]
    )

    vaccine_count = len(
        {
            (
                e["code"],
                e["event_date"]
            )
            for e in user["events"]
            if e.get("type") == "vaccine"
        }
    )

    text = (
        f"👶 {user['child_name']}\n\n"
        f"📅 Дата рождения:\n"
        f"{format_date(user['birth_date'])}\n\n"
        f"🧠 Скачков развития: "
        f"{growth_count}\n"
        f"🎉 Поздравлений: "
        f"{milestone_count}\n"
        f"💉 Прививок: "
        f"{vaccine_count}"
    )

    await message.answer(
        text
    )