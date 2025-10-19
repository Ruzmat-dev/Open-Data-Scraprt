import aiohttp
from aiogram import types
from aiogram.filters import Command

async def cmd_latest(message: types.Message):
    await message.answer("⏳ So‘nggi natijalar yuklanmoqda...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/jobs/jobs/?limit=5") as resp:
                data = await resp.json()

        if not data:
            await message.answer("⚠️ Hech qanday ma’lumot topilmadi.")
            return

        text = "📰 So‘nggi 5 ta natija:\n\n"
        for item in data[:5]:
            text += f"• {item.get('title', 'Noma’lum')} — {item.get('company', '—')}\n"

        await message.answer(text)

    except Exception as e:
        await message.answer(f"❌ Ma’lumot olishda xatolik: {e}")
