import aiohttp
from aiogram import types

async def cmd_latest(message: types.Message):
    await message.answer("⏳ So‘nggi natijalar yuklanmoqda...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/jobs/jobs/?limit=5") as resp:
                data = await resp.json()

        # 🔍 Agar data dict bo‘lsa, results ni olamiz, aks holda list bo‘lsa, to‘g‘ridan-to‘g‘ri ishlatamiz
        if isinstance(data, dict):
            results = data.get("results", [])
        else:
            results = data  # data o‘zi list bo‘lsa

        if not results:
            await message.answer("⚠️ Hech qanday ma’lumot topilmadi.")
            return

        text = "📰 So‘nggi 5 ta e’lon:\n\n"
        for item in results[:5]:
            text += (
                f"• 💼 <b>{item.get('title', 'Noma’lum lavozim')}</b>\n"
                f"🏢 {item.get('company', '—')}\n\n"
            )

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"❌ Ma’lumot olishda xatolik: <code>{e}</code>", parse_mode="HTML")
