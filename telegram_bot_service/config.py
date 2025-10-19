import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8362846732:AAGwLgZ3Y57l5dj7wQ9oL3-yATWh_eN0gek"
BASE_API_URL = os.getenv("API_URL")

# Endpoints
JOBS_ENDPOINT = f"{BASE_API_URL}/jobs"
