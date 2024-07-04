import asyncio
from aiogram import Bot, Dispatcher
import config
from virazh_bot.admin.admin_messages import router as admin_router
from virazh_bot.bot_init import bot, dp
import db

async def bot_starter():
    print('virazh running')
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    await db.initialize()
    await bot_starter()

if __name__ == '__main__':
    print('virazh bot running')
    asyncio.run(main())
