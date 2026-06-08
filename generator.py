import json

from datetime import (
    datetime,
    timedelta
)

from dateutil.relativedelta import (
    relativedelta
)


TEMPLATE_FILE = "growth_spurts.json"


def load_templates():

    with open(
        TEMPLATE_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def generate_month_events(
        birth
):

    events = []

    for month in range(1, 13):

        event_date = (
            birth +
            relativedelta(
                months=month
            )
        )

        if month == 12:

            title = "🎂 1 год"

        else:

            title = (
                f"🎉 {month} месяц"
            )

        events.append(
            {
                "type": "milestone",

                "code":
                    f"month_{month}",

                "title":
                    title,

                "event_date":
                    event_date.isoformat(),

                #
                # Для поздравлений
                # уведомление приходит
                # в день события
                #
                "date":
                    event_date.isoformat(),

                "sent":
                    False
            }
        )

    return events


def generate_events(
        birth_date: str
):

    birth = datetime.strptime(
        birth_date,
        "%Y-%m-%d"
    ).date()

    templates = load_templates()

    events = []

    #
    # Скачки развития
    #
    for template in templates:

        event_date = (
            birth +
            timedelta(
                days=template["offset_days"]
            )
        )

        notify_date = (
            event_date -
            timedelta(days=1)
        )

        events.append(
            {
                "type": "growth",

                "code":
                    template["code"],

                "title":
                    template["title"],

                "event_date":
                    event_date.isoformat(),

                #
                # Предупреждение
                # за день
                #
                "date":
                    notify_date.isoformat(),

                "sent":
                    False
            }
        )

    #
    # Ежемесячные события
    #
    events.extend(
        generate_month_events(
            birth
        )
    )

    #
    # Сортировка по дате события
    #
    return sorted(
        events,
        key=lambda x:
        x["event_date"]
    )
