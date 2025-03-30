# import asyncio
#
# from virazh_bot import bot
#
# asyncio.run(bot.main())

import asyncio
from integration import vk
from config import vk_token
import aiohttp

from config import vk_token
peer_id = 299464016


async def upload_photo():
    async with aiohttp.ClientSession() as session:
        # Получение сервера для загрузки
        async with session.get(
                "https://api.vk.com/method/photos.getMessagesUploadServer",
                params={"access_token": vk_token, "v": "5.131"}, ssl=False
        ) as resp:
            upload_url = (await resp.json())["response"]["upload_url"]

        # Загрузка файла
        with open("image.png", "rb") as file:
            async with session.post(upload_url, data={"photo": file}, ssl=False) as resp:
                upload_data = await resp.json()

        # Сохранение фото
        async with session.get(
                "https://api.vk.com/method/photos.saveMessagesPhoto",
                params={"access_token": vk_token, "v": "5.131", **upload_data}, ssl=False
        ) as resp:
            photo = (await resp.json())["response"][0]

    return f"photo{photo['owner_id']}_{photo['id']}"


async def send_photo():
    attachment = await upload_photo()
    async with aiohttp.ClientSession() as session:
        await session.get(
            "https://api.vk.com/method/messages.send",
            params={
                "access_token": vk_token,
                "v": "5.131",
                "peer_id": peer_id,
                "attachment": attachment,
                "random_id": 0,
            }, ssl=False
        )


asyncio.run(send_photo())
