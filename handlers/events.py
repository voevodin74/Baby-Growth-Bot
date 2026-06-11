from datetime import datetime

from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message
)

from storage import (
    load_user
)

from generator import (
    load_templates
)

from utils import (
    format_date,
    format_week_range
)

router = Router()


@router.message(
    F.text == "📅 Ближайшие события"
)
async def next_events(
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

    templates = {
        item["code"]: item
        for item in load_templates()
    }

    today = datetime.now().date()

    future_events = []

    for event in user["events"]:

        event_date = datetime.strptime(
            event["event_date"],
            "%Y-%m-%d"
        ).date()

        if event_date >= today:

            future_events.append(
                event
            )

    future_events.sort(
        key=lambda x:
        x["event_date"]
    )

    #
    # Убираем дубли прививок
    #
    unique_events = []

    seen_vaccines = set()

    for event in future_events:

        if event.get(
                "type"
        ) == "vaccine":

            key = (
                event["code"],
                event["event_date"]
            )

            if key in seen_vaccines:
                continue

            seen_vaccines.add(
                key
            )

        unique_events.append(
            event
        )

    future_events = unique_events

    if not future_events:

        await message.answer(
            "Предстоящих событий нет."
        )

        return

    text = (
        "📅 Ближайшие события\n\n"
    )

    for event in future_events[:5]:

        #
        # Поздравления
        #
        if event.get(
                "type"
        ) == "milestone":

            text += (
                f"{event['title']}\n"
                f"📆 "
                f"{format_date(event['event_date'])}\n\n"
                "━━━━━━━━━━━━\n\n"
            )

            continue

        #
        # Прививки
        #
        if event.get(
                "type"
        ) == "vaccine":

            text += (
                f"💉 {event['title']}\n"
                f"📆 "
                f"{format_date(event['event_date'])}\n\n"
                "━━━━━━━━━━━━\n\n"
            )

            continue

        #
        # Скачки развития
        #
        template = templates[
            event["code"]
        ]

        text += (
            f"🧠 {template['title']}\n"
            f"📆 "
            f"{format_date(event['event_date'])}\n"
            f"👶 Возраст: "
            f"{format_week_range(template)}\n\n"
            f"{template['description']}\n\n"
        )

        text += (
            "Что вы можете заметить:\n"
        )

        for sign in template[
            "possible_signs"
        ]:

            text += (
                f"• {sign}\n"
            )

        text += (
            "\nНовые навыки:\n"
        )

        for skill in template[
            "new_skills"
        ]:

            text += (
                f"• {skill}\n"
            )

        text += (
            "\nСоветы:\n"
        )

        for tip in template[
            "tips"
        ]:

            text += (
                f"• {tip}\n"
            )

        text += (
            "\n━━━━━━━━━━━━\n\n"
        )

    await message.answer(
        text
    )