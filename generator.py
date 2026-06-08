import json

from datetime import datetime, timedelta


TEMPLATE_FILE = "growth_spurts.json"


def load_templates():

    with open(
        TEMPLATE_FILE,
        encoding="utf-8"
    ) as f:
        return json.load(f)


def generate_events(
        birth_date: str
):

    birth = datetime.strptime(
        birth_date,
        "%Y-%m-%d"
    ).date()

    templates = load_templates()

    events = []

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
                "code": template["code"],
                "title": template["title"],
                "event_date":
                    event_date.isoformat(),
                "date":
                    notify_date.isoformat(),
                "sent": False
            }
        )

    return events
