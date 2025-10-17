import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from services.api_client import get_data  # async versiya bo‘lishi kerak

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔘 Klaviatura (menu)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/data"), KeyboardButton(text="/latest")],
        [KeyboardButton(text="🔍 Qidiruv")],
    ],
    resize_keyboard=True,
)


# /start komandasi
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Salom! Men sizning botingizman 🤖\n"
        "Quyidagi buyruqlardan foydalaning:",
        reply_markup=main_keyboard,
    )

# /data komandasi
@dp.message(Command("data"))
async def send_data(message: types.Message):
    try:
        data = await get_data("jobs/")  # async bo‘lishi kerak
        await message.answer(f"📦 Backenddan ma'lumot:\n{data}")
    except Exception as e:
        await message.answer(f"⚠️ Xatolik yuz berdi:\n{e}")

# 🔍 Qidiruv tugmasi
@dp.message(F.text == "🔍 Qidiruv")
async def ask_for_search(message: types.Message):
    await message.answer(
        "<b>🔍 Qidiruv</b>\n\n"
        "Iltimos, qidiruv so‘rovini kiriting.\n"
        "Masalan: <i>Python</i>",
        parse_mode="HTML"
    )

# /latest komandasi — backenddan so‘nggi ma’lumotlar
@dp.message(Command("latest"))
async def cmd_latest(message: types.Message):
    await message.answer("⏳ So‘nggi natijalar yuklanmoqda...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/jobs/jobs/?limit=5") as resp:
                data = await resp.json()
        print(data)
        if not data:
            await message.answer("⚠️ Hech qanday ma’lumot topilmadi.")
            return

        text = "📰 So‘nggi 5 ta natija:\n\n"
        for item in data[:5]:
            text += f"• {item.get('title', 'Noma’lum')} — {item.get('company', '—')}\n"

        await message.answer(text)

    except Exception as e:
        await message.answer(f"❌ Ma’lumot olishda xatolik: {e}")

# Qidiruv funksiyasi (matn kiritsa)
@dp.message()
async def handle_search(message: types.Message):
    query = message.text.strip()

    # faqat matn (buyruq emas)
    if not query.startswith("/"):
        try:
            data = await get_data(f"jobs/?search={query}")

            if not data:
                await message.answer("⚠️ Hech qanday natija topilmadi.")
                return

            text_list = []
            for job in data[:5]:
                text = (
                    f"💼 <b>{job.get('title', 'Noma’lum lavozim')}</b>\n"
                    f"🏢 <b>Kompaniya:</b> {job.get('company', '—')}\n"
                    f"🌍 <b>Manba:</b> {job.get('source', '—')}\n"
                    f"📅 <b>Sana:</b> {job.get('posted_at', '')[:10]}\n\n"
                    f"🔗 <a href='{job.get('url')}'>E’lonni ko‘rish</a>"
                )
                text_list.append(text)

            await message.answer(
                "🔍 <b>Qidiruv natijalari:</b>\n\n" +
                "\n\n────────────\n\n".join(text_list),
                parse_mode="HTML",
                disable_web_page_preview=True
            )

        except Exception as e:
            await message.answer(f"⚠️ Xatolik yuz berdi:\n<code>{e}</code>", parse_mode="HTML")
    else:
        await message.answer("❗ Noma’lum buyruq. Iltimos, matn kiriting (masalan: Python).")

# 🔁 Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
