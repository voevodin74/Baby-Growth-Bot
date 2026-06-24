import os
import asyncio

from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from aiogram import Bot
from aiogram import Dispatcher

from aiogram.fsm.storage.memory import (
    MemoryStorage
)

from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)

from scheduler import (
    check_events,
    refresh_events
)

from handlers.menu import (
    router as menu_router
)

from handlers.calendar import (
    router as calendar_router
)

from handlers.child import (
    router as child_router
)

from handlers.events import (
    router as events_router
)

from handlers.birth_date import (
    router as birth_date_router
)

from handlers.delete_child import (
    router as delete_child_router
)

from handlers.about import (
    router as about_router
)


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)

dp = Dispatcher(
    storage=MemoryStorage()
)

scheduler = AsyncIOScheduler()

#
# Подключение роутеров
#
dp.include_router(
    menu_router
)

dp.include_router(
    calendar_router
)

dp.include_router(
    child_router
)

dp.include_router(
    events_router
)

dp.include_router(
    birth_date_router
)

dp.include_router(
    delete_child_router
)

dp.include_router(
    about_router
)


async def scheduled_check():

    await check_events(
        bot
    )

async def scheduled_refresh():

    await refresh_events()    


async def on_startup():

    #
    # Обновление календарей
    #
    scheduler.add_job(
        scheduled_refresh,
        "cron",
        hour=9,
        minute=0,
        timezone=ZoneInfo(
            "Europe/Moscow"
        )
    )

    #
    # Рассылка уведомлений
    #
    scheduler.add_job(
        scheduled_check,
        "cron",
        hour=10,
        minute=0,
        timezone=ZoneInfo(
            "Europe/Moscow"
        )
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