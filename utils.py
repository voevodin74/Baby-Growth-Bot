from datetime import datetime


def format_date(
        date_string: str
):

    return datetime.strptime(
        date_string,
        "%Y-%m-%d"
    ).strftime(
        "%d.%m.%Y"
    )


def format_week_range(
        template: dict
):

    start_week = (
        template["offset_days"] // 7
    )

    end_week = (
        template["offset_days"] +
        template["duration_days"]
    ) // 7

    return (
        f"{start_week}–{end_week} нед."
    )