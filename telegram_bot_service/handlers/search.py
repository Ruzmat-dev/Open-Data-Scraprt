from aiogram import types, F
from services.api_client import get_data

async def ask_for_search(message: types.Message):
    await message.answer(
        "<b>🔍 Qidiruv</b>\n\n"
        "Iltimos, qidiruv so‘rovini kiriting.\n"
        "Masalan: <i>Python</i>",
        parse_mode="HTML"
    )


async def handle_search(message: types.Message):
    query = message.text.strip()

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
