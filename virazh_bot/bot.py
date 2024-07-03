import asyncio
from aiogram import Bot, Dispatcher
import config
from virazh_bot.admin.admin_messages import router as admin_router
from virazh_bot.bot_init import bot, dp

dp.include_router(admin_router)

async def bot_starter():
    print('virazh running')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('virazh bot running')
    asyncio.run(bot_starter())
