from database import db
from asyncpg import create_pool

tg_admin = db.tg_admins()
menu = db.menu()
categories = db.categories()
users = db.users()
orders = db.orders()
images = db.images()
text_table = db.text_table()
async def initialize(folder = 'database/'):
    db = await create_pool(user='gen_user', password='mGk-base)=-', database='default_db', host="82.97.248.66")
    # db = await asyncpg.connect(
    #     host="82.97.248.66",
    #     database="default_db",
    #     user="gen_user",
    #     password="mGk-base)=-"
    # )
    await tg_admin.connect(db)
    await tg_admin.create_table()
    await menu.connect(db)
    await menu.create_table()
    await categories.connect(db)
    await categories.create_table()
    await users.connect(db)
    await users.create_table()
    await orders.connect(db)
    await orders.create_table()
    await images.connect(db)
    await images.create_table()
    await text_table.connect(db)
    await text_table.create_table()
