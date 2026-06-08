import calendar
from datetime import datetime

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


MONTHS = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
]


def create_calendar(year=None, month=None):

    now = datetime.now()

    year = year or now.year
    month = month or now.month

    kb = []

    kb.append([
        InlineKeyboardButton(
            text=f"{MONTHS[month-1]} {year}",
            callback_data="ignore"
        )
    ])

    kb.append([
        InlineKeyboardButton(text="Пн", callback_data="ignore"),
        InlineKeyboardButton(text="Вт", callback_data="ignore"),
        InlineKeyboardButton(text="Ср", callback_data="ignore"),
        InlineKeyboardButton(text="Чт", callback_data="ignore"),
        InlineKeyboardButton(text="Пт", callback_data="ignore"),
        InlineKeyboardButton(text="Сб", callback_data="ignore"),
        InlineKeyboardButton(text="Вс", callback_data="ignore"),
    ])

    cal = calendar.monthcalendar(year, month)

    for week in cal:

        row = []

        for day in week:

            if day == 0:

                row.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data="ignore"
                    )
                )

            else:

                row.append(
                    InlineKeyboardButton(
                        text=str(day),
                        callback_data=f"day:{year}:{month}:{day}"
                    )
                )

        kb.append(row)

    kb.append([
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev:{year}:{month}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next:{year}:{month}"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=kb
    )
