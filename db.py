from database import db
from config import database_folder

order = db.orders()
tg_admin = db.tg_admins()
async def initialize():
    await order.connect()
    await tg_admin.connect()
