from database import db
from config import database_folder

order = db.orders()
tg_admin = db.tg_admins()
menu = db.menu()
categories = db.categories()
users = db.users()
orders = db.orders()
async def initialize(folder = 'database/'):
    await order.connect(folder)
    await tg_admin.connect(folder)
    await menu.connect(folder)
    await categories.connect(folder)
    await users.connect()
    await orders.connect()
