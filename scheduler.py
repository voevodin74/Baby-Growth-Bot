import json

from datetime import date

from aiogram import Bot

from storage import USERS_DIR

from generator import generate_events


def build_growth_message(
        template
):

    text = (
        "👶 Завтра ожидается скачок развития\n\n"
        f"📈 {template['title']}\n\n"
        f"{template['description']}\n\n"
    )

    text += (
        "Что вы можете заметить:\n"
    )

    for item in template[
        "possible_signs"
    ]:

        text += f"• {item}\n"

    text += (
        "\nВозможные новые навыки:\n"
    )

    for item in template[
        "new_skills"
    ]:

        text += f"• {item}\n"

    text += "\nСоветы:\n"

    for item in template[
        "tips"
    ]:

        text += f"• {item}\n"

    return text


def build_milestone_message(
        event
):

    month = (
        event["code"]
        .replace(
            "month_",
            ""
        )
    )

    if month == "12":

        return (
            "🎂 Сегодня первый день рождения!\n\n"
            "Поздравляем вашу семью с этим "
            "важным событием ❤️\n\n"
            "Целый год удивительных открытий, "
            "роста и счастливых моментов уже "
            "позади. Пусть впереди будет ещё "
            "больше радости и новых достижений."
        )

    return (
        f"🎉 Сегодня малышу исполнился "
        f"{month} месяц!\n\n"
        "Каждый месяц приносит новые "
        "открытия, навыки и счастливые "
        "моменты.\n\n"
        "Поздравляем вашу семью "
        "с этой маленькой, но важной датой ❤️"
    )



def build_vaccine_message(
        event
):

    event_date = (
        event["event_date"]
        .replace("-", ".")
    )

    if (
        event.get("notify_type")
        == "week"
    ):

        return (
            "💉 Через неделю плановая вакцинация\n\n"

            f"📅 {event_date}\n\n"

            "Согласно календарю "
            "профилактических прививок "
            "наступает срок вакцинации:\n\n"

            f"{event['title']}\n\n"

            f"{event['description']}\n\n"

            "Рекомендуется заранее "
            "записаться к педиатру "
            "и убедиться в отсутствии "
            "противопоказаний."
        )

    return (
        "💉 Завтра плановая вакцинация\n\n"

        f"📅 {event_date}\n\n"

        "Согласно календарю "
        "профилактических прививок "
        "необходимо выполнить:\n\n"

        f"{event['title']}\n\n"

        f"{event['description']}\n\n"

        "Подготовьте документы "
        "и уточните время посещения "
        "поликлиники."
    )


async def check_events(
        bot: Bot
):

    today = (
        date.today()
        .isoformat()
    )

    with open(
        "growth_spurts.json",
        encoding="utf-8"
    ) as f:

        templates = json.load(f)

    template_map = {
        item["code"]: item
        for item in templates
    }

    for file in USERS_DIR.glob(
        "*.json"
    ):

        with open(
            file,
            encoding="utf-8"
        ) as f:

            user = json.load(f)

        changed = False

        for event in user["events"]:

            if (
                event["date"] == today
                and not event["sent"]
            ):

                #
                # Скачки развития
                #
                if (
                    event.get("type")
                    == "growth"
                ):

                    template = (
                        template_map[
                            event["code"]
                        ]
                    )

                    await bot.send_message(
                        user["telegram_id"],
                        build_growth_message(
                            template
                        )
                    )

                #
                # Ежемесячные поздравления
                #
                elif (
                    event.get("type")
                    == "milestone"
                ):

                    await bot.send_message(
                        user["telegram_id"],
                        build_milestone_message(
                            event
                        )
                    )

                #
                # Прививки
                #
                elif (
                    event.get("type")
                    == "vaccine"
                ):

                    await bot.send_message(
                        user["telegram_id"],
                        build_vaccine_message(
                            event
                        )
                    )

                event["sent"] = True

                changed = True

        if changed:

            with open(
                file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    user,
                    f,
                    ensure_ascii=False,
                    indent=2
                )


async def refresh_events():

    for file in USERS_DIR.glob("*.json"):

        with open(
            file,
            encoding="utf-8"
        ) as f:

            user = json.load(f)

        #
        # Запоминаем уже отправленные события
        #
        sent_map = {
            (
                event["type"],
                event["code"],
                event["date"]
            ): event["sent"]
            for event in user["events"]
        }

        #
        # Полностью пересчитываем календарь
        #
        new_events = generate_events(
            user["birth_date"]
        )

        #
        # Возвращаем статус отправки
        #
        for event in new_events:

            key = (
                event["type"],
                event["code"],
                event["date"]
            )

            event["sent"] = sent_map.get(
                key,
                False
            )

        user["events"] = new_events

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                user,
                f,
                ensure_ascii=False,
                indent=2
            )