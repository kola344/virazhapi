import aiohttp
import asyncio
from config import vk_token, vk_id, vk_username # Замените на ваш ID пользователя


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