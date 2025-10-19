from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.api_client import get_data

# 🧠 Har bir foydalanuvchi uchun vaqtinchalik natijalarni saqlash
user_search_cache = {}


# 🧩 1️⃣ Ish e’loni uchun matn tayyorlovchi funksiya (component)
def format_job_text(idx: int, job: dict) -> str:
    """Ish e’loni ma’lumotlarini formatlab beradi."""
    text = (
        f"{idx}. 💼 <b>{job.get('title', 'Noma’lum lavozim')}</b>\n"
        f"🏢 <b>Kompaniya:</b> {job.get('company', '—')}\n"
        f"📅 <b>Sana:</b> {job.get('posted_at', '')[:10]}\n"
    )

    url = job.get("url")
    if url:
        text += f"🔗 <a href='{url}'>E’lonni ko‘rish</a>\n"
    return text


# 🔍 2️⃣ Qidiruvni so‘rash
async def ask_for_search(message: types.Message):
    await message.answer(
        "<b>🔍 Qidiruv</b>\n\n"
        "Iltimos, qidiruv so‘rovini kiriting.\n"
        "Masalan: <i>Python</i>",
        parse_mode="HTML"
    )


# 🔍 3️⃣ Qidiruv natijalarini olish (pagination bilan)
async def handle_search(message: types.Message):
    query = message.text.strip()

    if query.startswith("/"):
        return await message.answer("❗ Noma’lum buyruq. Matn kiriting (masalan: Python).")

    try:
        data = await get_data(f"jobs/?search={query}")
        print("✅ Qidiruv natijasi:", data)

        if not data:
            return await message.answer("⚠️ Hech qanday natija topilmadi.")

        # 🔹 Natijalarni userga bog‘laymiz
        user_search_cache[message.from_user.id] = {
            "query": query,
            "results": data,
        }

        # 🔹 Birinchi sahifani ko‘rsatamiz
        await show_page(message, 0, data)

    except Exception as e:
        await message.answer(f"⚠️ Xatolik yuz berdi:\n<code>{e}</code>", parse_mode="HTML")


# 📄 4️⃣ Sahifani ko‘rsatish
async def show_page(message_or_callback, page: int, data: list, edit=False):
    per_page = 5
    start = page * per_page
    end = start + per_page
    page_data = data[start:end]

    # 📜 Matnni yig‘amiz (component yordamida)
    text_list = [format_job_text(idx, job) for idx, job in enumerate(page_data, start=start + 1)]

    total_pages = (len(data) - 1) // per_page + 1
    text_output = (
        f"🔍 <b>Qidiruv natijalari</b>\n\n"
        + "\n────────────\n".join(text_list)
        + f"\n\n📄 Sahifa: {page + 1}/{total_pages}"
    )

    # ⏩ Tugmalar
    kb = InlineKeyboardBuilder()
    if page > 0:
        kb.button(text="⬅️ Oldingi", callback_data=f"page:{page-1}")
    if end < len(data):
        kb.button(text="➡️ Keyingi", callback_data=f"page:{page+1}")
    kb.adjust(2)

    # 🔁 Edit yoki yangi xabar
    if edit:
        await message_or_callback.message.edit_text(
            text_output,
            reply_markup=kb.as_markup(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        await message_or_callback.answer(
            text_output,
            reply_markup=kb.as_markup(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )


# ⚙️ 5️⃣ Callback handler (pagination uchun)
async def handle_pagination(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_search_cache:
        return await callback.answer("❗ Ma’lumot topilmadi, qayta qidiring.", show_alert=True)

    data = user_search_cache[user_id]["results"]

    try:
        _, page_str = callback.data.split(":")
        page = int(page_str)
        await show_page(callback, page, data, edit=True)
    except Exception as e:
        await callback.answer(f"⚠️ Xatolik: {e}")
