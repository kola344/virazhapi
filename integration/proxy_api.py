import aiohttp
from config import proxyapi_key, gpt_prompt
from virazh_bot.ads.models import AdsSettings
from routers.api.users.cart_data import gift_target

async def get_balance() -> int:
    headers = {
        "Authorization": f"Bearer {proxyapi_key}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.proxyapi.ru/proxyapi/balance", headers=headers, ssl=False) as response:
            if response.status == 200:
                data = await response.json()
                return data['balance']
            return 0

async def generate_ad(ad: AdsSettings):
    info = ''
    if ad.selected["date"]:
        info += f'Дата: {ad.date}\n'
    if ad.selected["day_week"]:
        info += f'День недели: {ad.day_week}\n'
    if ad.selected["season"]:
        info += f'Сезон: {ad.season}\n'
    if ad.selected["weather"]:
        info += f"Погода: {ad.gift}\n"
    if ad.selected["gift"]:
        info += f"Подарок: {ad.gift} при заказе от {gift_target} рублей\n"
    if ad.item != "Не задано":
        info += f"Рекламируемый товар: {ad.item}\n"
    if ad.prompt != "Не задано":
        info += f"Дополнительный промпт: {ad.prompt}\n"

    prompt = gpt_prompt.replace('%info%', info)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {proxyapi_key}"
    }
    json = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.proxyapi.ru/openai/v1/chat/completions', ssl=False, headers=headers, json=json) as response:
            if response.status == 200:
                return (await response.json())["choices"][0]["message"]["content"]
            return "⚠️ Ошибка в генерации"

