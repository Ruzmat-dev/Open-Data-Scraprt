FROM python:3.12-slim

# Ishchi papka
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Barcha fayllarni ko‘chiramiz
COPY . .

# Django serverni ishga tushiramiz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
