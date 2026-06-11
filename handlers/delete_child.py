from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)

from storage import (
    load_user,
    delete_user
)

from keyboards import (
    MAIN_MENU,
    DELETE_MENU
)

router = Router()


@router.message(
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


@router.message(
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


@router.message(
    F.text == "❌ Отмена"
)
async def delete_cancel(
        message: Message
):

    await message.answer(
        "Удаление отменено.",
        reply_markup=MAIN_MENU
    )