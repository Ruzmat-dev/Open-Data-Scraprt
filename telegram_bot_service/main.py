import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from config import BOT_TOKEN

# Handlers import
from handlers.start import start_command
from handlers.latest import cmd_latest
from handlers.search import ask_for_search, handle_search

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔹 Handlerlarni ro‘yxatdan o‘tkazamiz
def register_handlers():
    dp.message.register(start_command, F.text == "/start")
    dp.message.register(cmd_latest, F.text == "/latest")
    dp.message.register(ask_for_search, F.text == "🔍 Qidiruv")
    dp.message.register(handle_search)


async def main():
    register_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
