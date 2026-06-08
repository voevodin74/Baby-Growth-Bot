import json

from datetime import date

from aiogram import Bot

from storage import USERS_DIR


def build_message(template):

    text = (
        f"👶 {template['title']}\n\n"
        f"{template['description']}\n\n"
    )

    text += "Что вы можете заметить:\n"

    for item in template[
        "possible_signs"
    ]:

        text += f"• {item}\n"

    text += "\nНовые навыки:\n"

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

                template = (
                    template_map[
                        event["code"]
                    ]
                )

                await bot.send_message(
                    user["telegram_id"],
                    build_message(
                        template
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
