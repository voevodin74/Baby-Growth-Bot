from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👶 Мой ребенок")],
        [KeyboardButton(text="📅 Ближайшие события")],
        [KeyboardButton(text="🔄 Изменить дату рождения")],
        [KeyboardButton(text="🗑 Удалить ребенка")],
        [KeyboardButton(text="ℹ️ О боте")]
    ],
    resize_keyboard=True
)

DELETE_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Да, удалить")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)