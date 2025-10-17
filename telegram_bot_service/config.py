import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8362846732:AAF1mYOcJImfCmYqHeg5u8AQiwdyHyv13TY"
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/jobs/")
