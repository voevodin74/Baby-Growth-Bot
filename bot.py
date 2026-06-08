import os
import asyncio

from datetime import datetime

from dotenv import load_dotenv

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F

from aiogram.filters import CommandStart

from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import (
    State,
    StatesGroup
)

from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)

from generator import generate_events

from storage import (
    save_user,
    load_user,
    delete_user,
    user_exists
)

from scheduler import (
    check_events
)

from calendar_widget import (
    create_calendar
)


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)

dp = Dispatcher(
    storage=MemoryStorage()
)

scheduler = AsyncIOScheduler()


class Registration(StatesGroup):
    child_name = State()


MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="👶 Мой ребенок"
            )
        ],
        [
            KeyboardButton(
                text="📅 Ближайшие скачки"
            )
        ],
        [
            KeyboardButton(
                text="🔄 Изменить дату рождения"
            )
        ],
        [
            KeyboardButton(
                text="🗑 Удалить ребенка"
            )
        ],
        [
            KeyboardButton(
                text="ℹ️ О боте"
            )
        ]
    ],
    resize_keyboard=True
)

DELETE_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="✅ Да, удалить"
            )
        ],
        [
            KeyboardButton(
                text="❌ Отмена"
            )
        ]
    ],
    resize_keyboard=True
)


def format_date(
        date_string: str
):

    return datetime.strptime(
        date_string,
        "%Y-%m-%d"
    ).strftime(
        "%d.%m.%Y"
    )


@dp.message(CommandStart())
async def start(
        message: Message,
        state: FSMContext
):

    if user_exists(
            message.from_user.id
    ):

        await message.answer(
            "👶 Ребенок уже зарегистрирован",
            reply_markup=MAIN_MENU
        )

        return

    await message.answer(
        "Привет 👋\n\n"
        "Как зовут ребенка?",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        Registration.child_name
    )


@dp.message(
    Registration.child_name
)
async def child_name(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        child_name=message.text
    )

    await message.answer(
        "📅 Выберите дату рождения:",
        reply_markup=create_calendar()
    )


@dp.callback_query(
    F.data == "ignore"
)
async def ignore_callback(
        callback: CallbackQuery
):
    await callback.answer()


@dp.callback_query(
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


@dp.callback_query(
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


@dp.callback_query(
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


@dp.message(
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

    text = (
        f"👶 {user['child_name']}\n\n"
        f"📅 Дата рождения:\n"
        f"{format_date(user['birth_date'])}\n\n"
        f"📈 Всего скачков:\n"
        f"{len(user['events'])}"
    )

    await message.answer(
        text
    )


@dp.message(
    F.text == "📅 Ближайшие скачки"
)
async def next_events(
        message: Message
):

    user = load_user(
        message.from_user.id
    )

    if not user:
        return

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

    if not future_events:

        await message.answer(
            "Предстоящих скачков нет."
        )

        return

    text = (
        "📅 Ближайшие скачки\n\n"
    )

    for event in future_events[:5]:

        text += (
            f"• {event['title']}\n"
            f"{format_date(event['event_date'])}\n\n"
        )

    await message.answer(
        text
    )


@dp.message(
    F.text == "🔄 Изменить дату рождения"
)
async def change_birth_date(
        message: Message,
        state: FSMContext
):

    user = load_user(
        message.from_user.id
    )

    if not user:
        return

    await state.update_data(
        child_name=user[
            "child_name"
        ]
    )

    await message.answer(
        "📅 Выберите новую дату рождения:",
        reply_markup=create_calendar()
    )


@dp.message(
    F.text == "🗑 Удалить ребенка"
)
async def delete_confirm(
        message: Message
):

    user = load_user(
        message.from_user.id
    )

    if not user:
        return

    await message.answer(
        "⚠️ Вы уверены?\n\n"
        "Все данные будут удалены.",
        reply_markup=DELETE_MENU
    )


@dp.message(
    F.text == "✅ Да, удалить"
)
async def delete_yes(
        message: Message
):

    delete_user(
        message.from_user.id
    )

    await message.answer(
        "✅ Данные удалены\n\n"
        "Используйте /start "
        "для новой регистрации.",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(
    F.text == "❌ Отмена"
)
async def delete_cancel(
        message: Message
):

    await message.answer(
        "Удаление отменено.",
        reply_markup=MAIN_MENU
    )


@dp.message(
    F.text == "ℹ️ О боте"
)
async def about(
        message: Message
):

	await message.answer(
	    "👶 Бот помогает родителям "
	    "отслеживать скачки развития "
	    "ребенка и заранее получать "
	    "уведомления о предстоящих "
	    "этапах развития.\n\n"
	    "@voevodin74"
	)

async def scheduled_check():

    await check_events(
        bot
    )


async def on_startup():

    scheduler.add_job(
        scheduled_check,
        "interval",
        hours=1
    )

    scheduler.start()


async def main():

    await on_startup()

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
