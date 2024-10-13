import asyncio
from virazh_bot.admin.admin_messages import router as admin_router
from virazh_bot.user.user_messages import router as user_router
from virazh_bot.manager.manager_messages import router as manager_router
from virazh_bot.ads.ads_messages import router as ads_router
from virazh_bot.bot_init import bot, dp
import db

async def bot_starter():
    print('virazh running')
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(manager_router)
    dp.include_router(ads_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    await db.initialize()
    await bot_starter()

if __name__ == '__main__':
    print('virazh bot running')
    asyncio.run(main())
