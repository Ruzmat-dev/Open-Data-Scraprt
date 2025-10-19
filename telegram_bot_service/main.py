import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from config import BOT_TOKEN

# Handlers import
from handlers.start import start_command
from handlers.latest import cmd_latest
from handlers.search import ask_for_search, handle_search, handle_pagination

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def register_handlers():
    dp.message.register(start_command, F.text == "/start")
    dp.message.register(cmd_latest, F.text == "🔔 So‘nggi yangiliklar")
    dp.message.register(ask_for_search, F.text == "🔍 Qidiruv")
    dp.message.register(handle_search)
    dp.callback_query.register(handle_pagination, F.data.startswith("page:"))

async def main():
    register_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
