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
    db = await asyncpg.connect(
        host="82.97.248.66",
        database="default_db",
        user="gen_user",
        password="mGk-base)=-"
    )
    print(type(db))
    # await db.execute('''TRUNCATE TABLE tg_admins''')
    # await db.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
    #                     id SERIAL PRIMARY KEY,
    #                     user_id INT,
    #                     name TEXT)''')
    inserted_id = await db.fetchval('''INSERT INTO tg_admins (user_id, name) VALUES ($1, $2)''', 1659397548, 'Коля')
    # print(inserted_id)
    # fetched = await db.fetch('''SELECT id FROM tg_admins''')
    # print(fetched)
    # print([data[0] for data in fetched])

asyncio.run(run())