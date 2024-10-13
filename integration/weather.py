import aiohttp
from config import weather_url

async def get_weather():
    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url, ssl=False) as response:
            return await response.text()