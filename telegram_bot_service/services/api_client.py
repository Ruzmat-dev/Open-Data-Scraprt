import aiohttp

BASE_URL = "http://127.0.0.1:8000/"

async def get_data(endpoint: str):
    url = f"{BASE_URL}{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()
