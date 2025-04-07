import json

import aiohttp

import config
from config import vk_token, vk_id, vk_username # Замените на ваш ID пользователя
from datetime import datetime, timedelta
import asyncio
from virazh_bot.keygen import generate_birthdayPromo

async def upload_image(session, image_path):
    # Получаем URL для загрузки изображения
    upload_url = await get_upload_url(session)

    # Загружаем изображение на сервер VK
    with open(image_path, 'rb') as file:
        data = {'file1': file}
        async with session.post(upload_url, data=data, ssl=False) as upload_response:
            upload_result = await upload_response.json()

    # Сохраняем загруженное фото на стене
    photo = await save_wall_photo(session, upload_result)
    return photo


async def get_upload_url(session):
    url = f"https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": vk_token,
        "v": "5.131"
    }
    async with session.get(url, params=params, ssl=False) as response:
        result = await response.json()
        return result['response']['upload_url']


async def save_wall_photo(session, upload_result):
    url = f"https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": vk_token,
        "v": "5.131",
        "server": upload_result["server"],
        "photo": upload_result["photo"],
        "hash": upload_result["hash"]
    }
    async with session.post(url, params=params, ssl=False) as response:
        result = await response.json()
        photo = result['response'][0]
        return f"photo{photo['owner_id']}_{photo['id']}"


async def post_to_wall(session, message, photo_attachment = None):
    url = f"https://api.vk.com/method/wall.post"
    params = {
        "access_token": vk_token,
        "v": "5.131",
        "owner_id": vk_id,
        "message": message
    }
    if photo_attachment:
        params["attachments"] = photo_attachment
    async with session.post(url, params=params, ssl=False) as response:
        result = await response.json()
        post_id = result['response']['post_id']
        return f'https://vk.com/{vk_username}?w=wall{vk_id}_{post_id}'

async def publicate(text, image = False):
    async with aiohttp.ClientSession() as session:
        if image:
            # Загружаем изображение и получаем строку для attachments
            image_path = 'ad_temp/image.png'
            photo_attachment = await upload_image(session, image_path)

            # Публикуем запись на стене
            url = await post_to_wall(session, text, photo_attachment)
        else:
            url = await post_to_wall(session, text)
        return url

async def get_friends_where_birthday() -> list:
    async with aiohttp.ClientSession() as session:
        url = f"https://api.vk.com/method/friends.get"
        params = {
            "access_token": vk_token,
            "v": "5.131",
            "fields": "bdate"
        }
        async with session.post(url, params=params, ssl=False) as response:
            friends = (await response.json())['response']['items']
        params = {
            "access_token": vk_token,
            "v": "5.131",
            "fields": "bdate",
            'offset': 5000,
        }
        async with session.post(url, params=params, ssl=False) as response:
            friends += (await response.json())['response']['items']
        with open('friends.json', 'w') as f:
            json.dump(friends, f, indent=4, ensure_ascii=False)
        current_day = datetime.now().strftime('%d.%m')
        if current_day[0] == '0':
            current_day = current_day[1:]
        if current_day[-2] == '0':
            current_day = current_day[:-2] + current_day[-1]
        result_list = [user['id'] for user in friends if user.get('bdate') and user['bdate'].startswith(current_day) and not user.get('deactivated')]
        return result_list


async def upload_photo(photo_path):
    async with aiohttp.ClientSession() as session:
        # Получение сервера для загрузки
        async with session.get(
                "https://api.vk.com/method/photos.getMessagesUploadServer",
                params={"access_token": vk_token, "v": "5.131"},
        ) as resp:
            upload_url = (await resp.json())["response"]["upload_url"]

        # Загрузка файла
        with open(photo_path, "rb") as file:
            async with session.post(upload_url, data={"photo": file}) as resp:
                upload_data = await resp.json()

        # Сохранение фото
        async with session.get(
                "https://api.vk.com/method/photos.saveMessagesPhoto",
                params={"access_token": vk_token, "v": "5.131", **upload_data},
        ) as resp:
            photo = (await resp.json())["response"][0]

    return f"photo{photo['owner_id']}_{photo['id']}"


async def send_photo_to_friends(friends_ids: list, photo_path: str):
    attachment = await upload_photo(photo_path)
    async with aiohttp.ClientSession() as session:
        for friend_id in friends_ids:
            promo = await generate_birthdayPromo(10)
            await session.get(
                "https://api.vk.com/method/messages.send",
                params={
                    "access_token": vk_token,
                    "v": "5.131",
                    "peer_id": friend_id,
                    "attachment": attachment,
                    "random_id": 0,
                    "message": config.birthday_text.replcae('%p%', promo)
                },
            )
            await asyncio.sleep(5)
