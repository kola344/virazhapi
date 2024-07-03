from fastapi import FastAPI, Request
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
        return {"Status": True, "init": 'Success'}
    except Exception as e:
        return {"Status": False, "init": f"err: {e}"}

@app.post('/bot_hook')
async def webhook(request: Update):
    json_str = request.json()
    update = Update.to_object(json_str)
    await bot_init.dp.feed_update(bot_init.bot, update)
    # update = Update(**await request.json())
    # await bot_init.dp.feed_update(bot_init.bot, update)
    return {'status': 'ok'}

@app.on_event('startup')
async def on_startup():
    bot_init.dp.include_router(admin_router)
    await bot_init.bot.set_webhook(config.webhook_url)

@app.on_event('shutdown')
async def on_shutdown():
    await bot_init.bot.delete_webhook()
    await bot_init.bot.session.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5500)
