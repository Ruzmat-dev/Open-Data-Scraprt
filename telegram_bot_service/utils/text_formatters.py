
def format_job_text(job: dict, index: int | None = None) -> str:
    prefix = f"{index}. " if index else ""

    text = (
        f"{prefix}💼 <b>{job.get('title', 'Noma’lum lavozim')}</b>\n"
        f"🏢 <b>Kompaniya:</b> {job.get('company', '—')}\n"
        f"📅 <b>Sana:</b> {job.get('posted_at', '')[:10]}\n"
    )

    if job.get("url"):
        text += f"🔗 <a href='{job['url']}'>E’lonni ko‘rish</a>\n"

    return text
