import aiohttp
from aiogram import types
import html
from utils.text_formatters import format_job_text


async def cmd_latest(message: types.Message):
    await message.answer("⏳ So‘nggi natijalar yuklanmoqda...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/jobs/jobs/?limit=5") as resp:
                # statusni tekshirish foydali (500/404 holatlari uchun)
                if resp.status != 200:
                    text_body = await resp.text()
                    raise Exception(f"API status {resp.status}: {text_body}")

                data = await resp.json()

        # data dict bo'lsa 'results'ni olamiz, aks holda o'zi list deb hisoblaymiz
        results = data.get("results") if isinstance(data, dict) else data

        if not results:
            await message.answer("⚠️ Hech qanday ma’lumot topilmadi.")
            return

        # Matnni yig'ish (component yordamida)
        lines = []
        for i, item in enumerate(results[:5], start=1):
            lines.append(format_job_text(item, index=i))

        full_text = "📰 <b>So‘nggi 5 ta e’lon:</b>\n\n" + "\n".join(lines)

        await message.answer(full_text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        # xatolikni xavfsiz tarzda escape qilib ko'rsatamiz
        await message.answer(
            f"❌ Ma’lumot olishda xatolik:\n<code>{html.escape(str(e))}</code>",
            parse_mode="HTML"
        )