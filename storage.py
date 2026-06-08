import json

from pathlib import Path


USERS_DIR = Path("users")

USERS_DIR.mkdir(
    exist_ok=True
)


def user_file(
    telegram_id: int
):

    return (
        USERS_DIR /
        f"{telegram_id}.json"
    )


def save_user(data):

    with open(
        user_file(
            data["telegram_id"]
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_user(
    telegram_id: int
):

    file = user_file(
        telegram_id
    )

    if not file.exists():
        return None

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def delete_user(
    telegram_id: int
):

    file = user_file(
        telegram_id
    )

    if file.exists():
        file.unlink()


def user_exists(
    telegram_id: int
):

    return user_file(
        telegram_id
    ).exists()
