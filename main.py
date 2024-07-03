from fastapi import FastAPI, Request
from virazh_bot import bot
import asyncio
import db
from aiogram.types import Update
from virazh_bot import bot_init
import config
from virazh_bot.admin.admin_messages import router as admin_router

app = FastAPI()

@app.get('/')
async def index_page():
    try:
        await db.initialize()
        asyncio.run(bot.bot_starter())
        return {"Status": True, "init": 'Success'}
    except Exception as e:
        return {"Status": False, "init": f"err: {e}"}

@app.post('/bot_hook')
async def webhook(request: Update):
    update = Update(**await request.json())
    await bot_init.dp.feed_update(bot, update)
    return {'status': 'ok'}

@app.on_event('startup')
async def on_startup():
    await bot_init.bot.set_webhook(config.webhook_url)
    await bot_init.dp.include_router(admin_router)

@app.on_event('shutdown')
async def on_shutdown():
    await bot_init.bot.delete_webhook()
    await bot_init.bot.session.close()
