from aiogram import types
from keyboards.main_menu import main_keyboard

async def start_command(message: types.Message):
    await message.answer(
        "👋 Salom! Men sizning botingizman 🤖\n"
        "Quyidagi buyruqlardan foydalaning:",
        reply_markup=main_keyboard,
    )
