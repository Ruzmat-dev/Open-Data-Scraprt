import aiohttp
from config import BASE_API_URL

async def get_data(endpoint: str):
    url = f"{BASE_API_URL}/{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
