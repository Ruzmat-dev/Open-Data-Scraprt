from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔔 So‘nggi yangiliklar"), KeyboardButton(text="🔍 Qidiruv")]
    ],
    resize_keyboard=True,
)
