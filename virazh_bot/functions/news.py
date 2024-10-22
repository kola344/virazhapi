from virazh_bot.bot_init import bot
import db
import asyncio
from aiogram.types import FSInputFile

async def send_news(chat_id, message_id):
    users = await db.users.get_users_tg_ids()
    c = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user, from_chat_id=chat_id, message_id=message_id)
            c += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)
    return c, len(users)

async def send_news_by_gpt(text, image):
    users = await db.users.get_users_tg_ids()
    c = 0
    for user in users:
        try:
            if image:
                image_path = 'ad_temp/image.png'
                await bot.send_photo(chat_id=user, photo=FSInputFile(image_path), caption=text)
            else:
                await bot.send_message(chat_id=user, text=text)
            c += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)
    return c, len(users)
