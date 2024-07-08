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
    await db.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                        id SERIAL PRIMARY KEY,
                        user_id INT,
                        name TEXT)''')
    inserted_id = await db.fetchval('''INSERT INTO tg_admins (user_id, name) VALUES ($1, $2)''', 123, 'asdf')
    print(inserted_id)
    fetched = await db.fetch('''SELECT id FROM tg_admins''')
    print(fetched)
    print([data[0] for data in fetched])

asyncio.run(run())

import asyncpg
import json


import asyncpg
import json

import asyncpg
import json


import asyncpg
import json

class UserService:
    def __init__(self, db):
        self.db = db

    async def check_user_by_id(self, user_id):
        row = await self.db.fetchrow('SELECT 1 FROM users WHERE id = $1', user_id)
        return row is not None

    async def check_user_by_phone_number(self, phone_number):
        row = await self.db.fetchrow('SELECT 1 FROM users WHERE phone_number = $1', phone_number)
        return row is not None

    async def check_user_by_key(self, key):
        row = await self.db.fetchrow('SELECT 1 FROM users WHERE key = $1', key)
        return row is not None

    async def auth_user_phone(self, phone_number):
        if not await self.check_user_by_phone_number(phone_number):
            while True:
                key = generate_password(16)
                if not await self.check_user_by_key(key):
                    break
            await self.db.execute('INSERT INTO users (phone_number, key) VALUES ($1, $2)', phone_number, key)
            # No need for commit in asyncpg, `execute` is auto-committed
        auth_codes[phone_number] = generate_code()
        #await sms_code.send_code(phone_number)

        from virazh_bot.bot_init import bot
        await bot.send_message(-4253301518, f'Код подтверждения: {auth_codes[phone_number]}.')

    async def get_key_by_phone_number(self, phone_number):
        row = await self.db.fetchrow('SELECT key FROM users WHERE phone_number = $1', phone_number)
        return row['key'] if row else None

    async def get_phone_by_key(self, key):
        row = await self.db.fetchrow('SELECT phone_number FROM users WHERE key = $1', key)
        return row['phone_number'] if row else None

    async def get_tg_id_by_phone_number(self, phone_number):
        row = await self.db.fetchrow('SELECT tg_id FROM users WHERE phone_number = $1', phone_number)
        return row['tg_id'] if row else None

    async def get_user_data_by_key(self, key):
        row = await self.db.fetchrow('SELECT * FROM users WHERE key = $1', key)
        if row:
            return {
                "id": row['id'],
                "name": row['name'],
                "phone_number": row['phone_number'],
                "tg_id": row['tg_id'],
                "tg_first_name": row['tg_first_name'],
                "tg_last_name": row['tg_last_name'],
                "tg_username": row['tg_username'],
                "key": row['key'],
                "active_order": row['active_order']
            }
        return None

    async def get_user_active_order_by_key(self, key):
        row = await self.db.fetchrow('SELECT active_order FROM users WHERE key = $1', key)
        return row['active_order'] if row else None

    async def get_user_tg_id_by_key(self, key):
        row = await self.db.fetchrow('SELECT tg_id FROM users WHERE key = $1', key)
        return row['tg_id'] if row else None

    async def add_tg_data_with_key(self, key, tg_id, tg_first_name, tg_last_name, tg_username):
        await self.db.execute('''
            UPDATE users
            SET tg_id = $1, tg_first_name = $2, tg_last_name = $3, tg_username = $4
            WHERE key = $5
        ''', tg_id, tg_first_name, tg_last_name, tg_username, key)

    async def check_tg_connected_by_key(self, key):
        row = await self.db.fetchrow('SELECT tg_id FROM users WHERE key = $1', key)
        return row['tg_id'] is not None if row else False

    async def update_name_by_key(self, key, name):
        await self.db.execute('UPDATE users SET name = $1 WHERE key = $2', name, key)

    async def get_orders_history(self, key):
        rows = await self.db.fetch('SELECT * FROM orders WHERE order_by = $1', key)
        orders = []
        for order in rows:
            orders.append({
                "order_id": order['id'],
                "data": json.loads(order['data']),
                "text": order['text'],
                "delivery_at": order['delivery_at'],
                "comment": order['comment'],
                "order_by": order['order_by'],
                "address": order['address'],
                "status": order['status'],
                "date": order['date'],
                "price": order['price']
            })
        print(orders)
        return orders
