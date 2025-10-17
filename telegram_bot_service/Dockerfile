# Aiogram uchun Python image
FROM python:3.12-slim

# Ishchi papka
WORKDIR /app

# Kutubxonalarni o‘rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bot fayllarini nusxalaymiz
COPY . .

# Botni ishga tushiramiz
CMD ["python", "bot.py"]
