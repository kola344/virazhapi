# # import asyncio
# #
# # from virazh_bot import bot
# #
# # asyncio.run(bot.main())
#
# import psycopg2
#
#  conn = psycopg2.connect(
#     host="192.168.0.4",
#     database="default_db",
#     user="gen_user",
#     password="mGk-base)=-"
# )
import asyncpg
import asyncio
async def run():
    import db
    await db.initialize()
    await db.tg_admin.del_admin_by_id(8)
    await db.tg_admin.add_admin(123, 'bobik')
    print(await db.tg_admin.get_admins_list())

asyncio.run(run())