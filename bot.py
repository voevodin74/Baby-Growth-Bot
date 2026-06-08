import os

from datetime import datetime

from dotenv import load_dotenv

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F

from aiogram.filters import CommandStart

from aiogram.types import (
    Message,
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

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)

dp = Dispatcher(
    storage=MemoryStorage()
)

scheduler = AsyncIOScheduler()


class Registration(StatesGroup):
    child_name = State()
    birth_date = State()


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


@dp.message(CommandStart())
async def start(
        message: Message,
        state: FSMContext
):

    if user_exists(
            message.from_user.id
    ):

        await message.answer(
            "Ребенок уже зарегистрирован 👶",
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
        "Введите дату рождения ребенка.\n\n"
        "Формат:\n"
        "2024-01-15"
    )

    await state.set_state(
        Registration.birth_date
    )


@dp.message(
    Registration.birth_date
)
async def birth_date(
        message: Message,
        state: FSMContext
):

    try:

        datetime.strptime(
            message.text,
            "%Y-%m-%d"
        )

    except ValueError:

        await message.answer(
            "Неверный формат даты.\n\n"
            "Пример:\n"
            "2024-01-15"
        )

        return

    data = await state.get_data()

    events = generate_events(
        message.text
    )

    save_user(
        {
            "telegram_id":
                message.from_user.id,

            "child_name":
                data["child_name"],

            "birth_date":
                message.text,

            "events":
                events
        }
    )

    await state.clear()

    await message.answer(
        "✅ Ребенок успешно добавлен\n\n"
        "Теперь я буду напоминать "
        "о предстоящих скачках развития.",
        reply_markup=MAIN_MENU
    )


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
        f"{user['birth_date']}\n\n"
        f"📈 Скачков в календаре:\n"
        f"{len(user['events'])}"
    )

    await message.answer(text)


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

    future_events = sorted(
        user["events"],
        key=lambda x: x["date"]
    )

    text = (
        "📅 Ближайшие скачки\n\n"
    )

    for event in future_events[:5]:

        text += (
            f"• {event['title']}\n"
            f"{event['date']}\n\n"
        )

    await message.answer(text)


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
        "Все данные ребенка "
        "будут удалены.",
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
        "✅ Данные удалены.\n\n"
        "Для повторной регистрации "
        "используйте /start",
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
        "👶 Бот помогает отслеживать "
        "скачки развития ребенка.\n\n"
        "После регистрации вы будете "
        "получать автоматические "
        "уведомления о приближении "
        "важных этапов развития."
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

    import asyncio

    asyncio.run(
        main()
    )
