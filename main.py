from fastapi import FastAPI, Request
import asyncio
import db
from aiogram.types import Update
from virazh_bot.bot_init import bot, dp
import config
from virazh_bot.admin.admin_messages import router as admin_router
from aiogram import Bot, Dispatcher
from typing import Any

app = FastAPI()

@app.get('/')
async def index_page():
    try:
        return {"Status": True, "init": 'Success'}
    except Exception as e:
        return {"Status": False, "init": f"err: {e}"}

@app.post('/bot_hook')
async def webhook(update: dict[str, Any]):
    await dp.feed_webhook_update(bot=bot, update=Update(**update))
    return {'status': 'ok'}

@app.on_event('startup')
async def on_startup():
    await db.initialize()
    dp.include_router(admin_router)
    await bot.set_webhook(config.webhook_url)

@app.on_event('shutdown')
async def on_shutdown():
    pass
    #await bot_init.bot.delete_webhook()
    #await bot_init.bot.session.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5500)
