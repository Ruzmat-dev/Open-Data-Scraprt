from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.api_client import get_data

# Har bir foydalanuvchi uchun vaqtinchalik saqlash (oddiy variant)
user_search_cache = {}


# 🔍 Qidiruvni so‘rash
async def ask_for_search(message: types.Message):
    await message.answer(
        "<b>🔍 Qidiruv</b>\n\n"
        "Iltimos, qidiruv so‘rovini kiriting.\n"
        "Masalan: <i>Python</i>",
        parse_mode="HTML"
    )


# 🔍 Qidiruv natijalarini olish (pagination bilan)
async def handle_search(message: types.Message):
    query = message.text.strip()

    if query.startswith("/"):
        return await message.answer("❗ Noma’lum buyruq. Matn kiriting (masalan: Python).")

    try:
        data = await get_data(f"jobs/?search={query}")
        print("✅ Qidiruv natijasi:", data)  # 🔥 SHU YERGA QO‘Y

        if not data:
            return await message.answer("⚠️ Hech qanday natija topilmadi.")

        # Ma’lumotni saqlaymiz (key — user id)
        user_search_cache[message.from_user.id] = {
            "query": query,
            "results": data,
        }

        # Birinchi sahifani ko‘rsatamiz
        await show_page(message, 0, data)

    except Exception as e:
        await message.answer(f"⚠️ Xatolik yuz berdi:\n<code>{e}</code>", parse_mode="HTML")


# 🔢 Sahifani ko‘rsatish
async def show_page(message_or_callback, page: int, data: list, edit=False):
    per_page = 5
    start = page * per_page
    end = start + per_page
    page_data = data[start:end]

    # Matn yasaymiz
    text_list = []
    for idx, job in enumerate(page_data, start=start + 1):
        text = (
            f"{idx}. 💼 <b>{job.get('title', 'Noma’lum lavozim')}</b>\n"
            f"🏢 <b>Kompaniya:</b> {job.get('company', '—')}\n"
            f"📅 <b>Sana:</b> {job.get('posted_at', '')[:10]}\n"
        )
        if job.get("url"):
            text += f"🔗 <a href='{job['url']}'>E’lonni ko‘rish</a>\n"
        text_list.append(text)

    total_pages = (len(data) - 1) // per_page + 1
    text_output = (
        f"🔍 <b>Qidiruv natijalari</b>\n\n"
        + "\n────────────\n".join(text_list)
        + f"\n\n📄 Sahifa: {page + 1}/{total_pages}"
    )

    # Tugmalar
    kb = InlineKeyboardBuilder()
    if page > 0:
        kb.button(text="⬅️ Oldingi", callback_data=f"page:{page-1}")
    if end < len(data):
        kb.button(text="➡️ Keyingi", callback_data=f"page:{page+1}")
    kb.adjust(2)

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


# ⚙️ Callback query uchun handler
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
