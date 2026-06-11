from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message
)

router = Router()


@router.message(
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