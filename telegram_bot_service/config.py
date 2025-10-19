import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8362846732:AAF1mYOcJImfCmYqHeg5u8AQiwdyHyv13TY"
BASE_API_URL = os.getenv("API_URL")

# Endpoints
JOBS_ENDPOINT = f"{BASE_API_URL}/jobs"
