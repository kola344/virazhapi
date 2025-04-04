from fastapi import FastAPI, Request, Response, HTTPException
import db
from aiogram.types import Update
from virazh_bot.bot_init import bot, dp
import config
from virazh_bot.admin.admin_messages import router as admin_router
from virazh_bot.user.user_messages import router as user_router
from virazh_bot.manager.manager_messages import router as manager_router
from virazh_bot.ads.ads_messages import router as ads_router
from virazh_bot.user.luckytickets.messages import router as luckytickets_router
from typing import Any
from routers.api.info.menu import router as menu_router
from routers.api.users.auth import router as users_router
from routers.api.users.telegram import router as telegram_router
from routers.api.users.orders import router as orders_router
from routers.api.users.cart import router as cart_router
import os
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from virazh_bot.bot_logging import log_message
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.initialize()
    if not os.path.exists('images'):
        os.mkdir('images')
    for image in await db.images.get_images():
        if not os.path.exists(f'images/{image["item_id"]}'):
            with open(f'images/{image["item_id"]}.png', 'wb') as f:
                f.write(image["data"])
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(manager_router)
    dp.include_router(ads_router)
    dp.include_router(luckytickets_router)
    print('setting webhook')
    await bot.delete_webhook()
    await bot.set_webhook(config.webhook_url, drop_pending_updates=True)
    try:
        yield
    finally:
        await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

app.include_router(menu_router, prefix="/api/info/menu", tags=["menu"])
app.include_router(users_router, prefix="/api/users/auth", tags=["user_auth"])
app.include_router(telegram_router, prefix='/api/users/telegram', tags=["telegram"])
app.include_router(orders_router, prefix='/api/users/orders', tags=["orders"])
app.include_router(cart_router, prefix='/api/users/cart', tags=["cart"])

@app.get('/')
async def index_page():
    '''Ахахахахахахаххахахахахахахахахх'''
    try:
        await db.initialize()
        return {"Status": True, "init": 'Success'}
    except Exception as e:
        return {"Status": False, "init": f"err: {e}"}

@app.post('/bot_hook', include_in_schema=False)
async def webhook(update: dict[str, Any]):
    '''АХАХАХХАХАХАХАХАХАХАХ'''
    await dp.feed_webhook_update(bot=bot, update=Update(**update))
    return {'status': 'ok'}

@app.get('/images/{image}')
async def get_menu_imagesPage(image: str):
    file_path = f'images/{image}'
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse('icons/notfound.jpg')

@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Surrogate-Control"] = "no-store"
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5500)
