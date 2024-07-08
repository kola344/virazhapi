import asyncio

from virazh_bot import bot

asyncio.run(bot.main())

# import asyncpg
# import asyncio
# async def run():
#     import db
#     await db.initialize()
#     await db.tg_admin.add_admin(1659397548, 'Коля')
#     print(await db.tg_admin.get_admins_list())
#
# asyncio.run(run())

# import asyncpg
# import asyncio
# async def run():
#     db = await asyncpg.connect(
#         host="82.97.248.66",
#         database="default_db",
#         user="gen_user",
#         password="mGk-base)=-"
#     )
#     await db.execute("DROP TABLE orders")
#
# asyncio.run(run())