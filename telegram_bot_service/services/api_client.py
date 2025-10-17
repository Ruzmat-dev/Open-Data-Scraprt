import requests
from config import API_URL

def get_data(endpoint: str):
    """Backend API dan ma'lumot olish"""
    url = f"{API_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
