from database import db
from config import database_folder
import asyncpg

tg_admin = db.tg_admins()
menu = db.menu()
categories = db.categories()
users = db.users()
orders = db.orders()
async def initialize(folder = 'database/'):
    # db = await asyncpg.connect(
    #     host="82.97.248.66",
    #     database="default_db",
    #     user="gen_user",
    #     password="mGk-base)=-"
    # )
    await tg_admin.connect(folder)
    await menu.connect(folder)
    await categories.connect(folder)
    await users.connect()
    await orders.connect()
