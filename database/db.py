import time
import aiosqlite
import asyncio
import config
from virazh_bot.keygen import generate_password, generate_code
from temp.auth_code import auth_codes
import db as dbs
from integration import sms_code
import asyncpg
import json

#TG
class tg_admins:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                                 id SERIAL PRIMARY KEY,
                                 user_id INT,
                                 name TEXT)''')

    async def check_admin_by_id(self, admin_id):
        row = self.db.fetchrow('''SELECT 1 FROM tg_admins WHERE id = $1''', admin_id)
        return row is not None

    async def check_admin_by_user_id(self, user_id):
        row = await self.db.fetchrow('SELECT user_id FROM tg_admins WHERE user_id = $1', user_id)
        return row is not None

    async def add_admin(self, user_id, name):
        if not await self.check_admin_by_user_id(user_id):
            inserted_id = await self.db.fetchval('''INSERT INTO tg_admins (user_id, name) VALUES ($1, $2)''', user_id, name)

    async def get_admins_list(self):
        cursor = await self.db.fetch('''SELECT * FROM tg_admins''')
        return [dict(data) for data in cursor]

    async def get_admins_user_ids(self):
        cursor = await self.db.fetch('''SELECT user_id FROM tg_admins''')
        return [data[0] for data in cursor]

    async def del_admin_by_id(self, admin_id):
        if await self.check_admin_by_user_id(admin_id):
            await self.db.execute('''SELECT FROM tg_admins WHERE id = $1''', admin_id)

    async def get_admin_user_id_by_id(self, admin_id):
        row = await self.db.fetchrow('''SELECT user_id FROM tg_admins WHERE id = $1''', admin_id)
        return row["user_id"]

class orders:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS orders (
                                                 id SERIAL PRIMARY KEY,
                                                 data TEXT,
                                                 delivery_at TEXT,
                                                 comment TEXT,
                                                 order_by TEXT,
                                                 address TEXT,
                                                 status TEXT,
                                                 message_id INT,
                                                 closed INT,
                                                 date TEXT,
                                                 price INT,
                                                 message_user_id INT,
                                                 payment TEXT)''')

    async def add_order(self, data, delivery_at, comment, order_by, address, date, price, payment):
        new_id = await self.db.fetchval('''
            INSERT INTO orders (data, delivery_at, comment, order_by, address, status, closed, date, price, payment)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id
        ''', str(data), delivery_at, comment, order_by, address, "🕙 В обработке", 0, date, price, payment)
        return new_id

    async def update_text(self, order_id, text):
        await self.db.execute('''
            UPDATE orders SET text = $1 WHERE id = $2
        ''', text, order_id)

    async def update_message_user_id(self, order_id, message_id):
        await self.db.execute('''
            UPDATE orders SET message_user_id = $1 WHERE id = $2
        ''', message_id, order_id)

    async def update_message_id(self, order_id, message_id):
        await self.db.execute('''
            UPDATE orders SET message_id = $1 WHERE id = $2
        ''', message_id, order_id)

    async def set_status(self, status, order_id):
        await self.db.execute('''
            UPDATE orders SET status = $1 WHERE id = $2
        ''', status, order_id)

    async def get_order_data(self, order_id):
        row = await self.db.fetchrow('''
            SELECT * FROM orders WHERE id = $1
        ''', order_id)

        if row:
            # Преобразование строки data из JSON в Python объект
            data = eval(row['data'])
            return {
                "id": row['id'],
                "data": data,
                "text": row['text'],
                "delivery_at": row['delivery_at'],
                "comment": row['comment'],
                "order_by": row['order_by'],
                "type": row['type'],
                "address": row['address'],
                "status": row['status'],
                "message_id": row['message_id'],
                "closed": row['closed'],
                "date": row['date'],
                "price": row['price']
            }
        return None

    async def get_user_message_id(self, order_id):
        row = await self.db.fetchrow('''
            SELECT message_user_id FROM orders WHERE id = $1
        ''', order_id)
        return row['message_user_id'] if row else None

    async def get_text(self, order_id):
        row = await self.db.fetchrow('''
            SELECT text FROM orders WHERE id = $1
        ''', order_id)
        return row['text'] if row else None

    async def close_order(self, order_id):
        await self.db.execute('''
            UPDATE orders SET closed = $1 WHERE id = $2
        ''', 1, order_id)

class categories:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                                         id SERIAL PRIMARY KEY,
                                         name TEXT)''')

    async def check_category_by_name(self, name):
        row = await self.db.fetchrow('''
            SELECT 1 FROM categories WHERE name = $1
        ''', name)
        return row is not None

    async def check_category_by_id(self, category_id):
        row = await self.db.fetchrow('''
            SELECT 1 FROM categories WHERE id = $1
        ''', category_id)
        return row is not None

    async def get_category_by_id(self, category_id):
        row = await self.db.fetchrow('''
            SELECT * FROM categories WHERE id = $1
        ''', category_id)
        if row:
            return dict(row)
        return None

    async def get_categories(self):
        rows = await self.db.fetch('''
            SELECT * FROM categories
        ''')
        return [dict(row) for row in rows]

    async def add_category(self, name):
        if not await self.check_category_by_name(name):
            new_id = await self.db.fetchval('''
                INSERT INTO categories (name) VALUES ($1)
                RETURNING id
            ''', name)
            return new_id
        return None

    async def del_category(self, category_id):
        await self.db.execute('''
            DELETE FROM categories WHERE id = $1
        ''', category_id)
        # Assuming `menu_db` is an instance of another service
        menu_db = dbs.menu  # Adjust according to your actual implementation
        await menu_db.del_all_items(category_id)

class menu:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                                            id SERIAL PRIMARY KEY,
                                            name TEXT,
                                            info TEXT,
                                            subinfo TEXT,
                                            price TEXT,
                                            category INT,
                                            variations TEXT,
                                            image_url TEXT)''')

    async def get_menu_by_category_id(self, category_id):
        rows = await self.db.fetch('''
            SELECT * FROM menu WHERE category = $1
        ''', category_id)

        result = []
        for item in rows:
            prices = item['price'].split('::')
            variations = item['variations'].split('::')
            result.append({
                "id": item['id'],
                "name": item['name'],
                "info": item['info'],
                "subinfo": item['subinfo'],
                "price": prices,
                "category": item['category'],
                "variations": variations,
                "image_url": f'{config.main_url}/images/{item["id"]}.png'
            })
        return result

    async def get_menu_by_item_ids(self, item_ids):
        rows = await self.db.fetch('''
            SELECT * FROM menu WHERE id = ANY($1::int[])
        ''', item_ids)

        result = []
        for item in rows:
            prices = item['price'].split('::')
            variations = item['variations'].split('::')
            category_data = await dbs.categories.get_category_by_id(item['category'])
            result.append({
                "id": item['id'],
                "name": item['name'],
                "info": item['info'],
                "subinfo": item['subinfo'],
                "prices": prices,
                "category": category_data["name"],
                "variations": variations,
                "image_url": f'{config.main_url}/images/{item["id"]}.png'
            })
        return result

    async def add_item(self, category_id):
        new_id = await self.db.fetchval('''
            INSERT INTO menu (name, price, category, variations)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        ''', 'Позиция', 'Цена', category_id, 'Вариация')
        return new_id

    async def get_item_info_by_id(self, item_id):
        row = await self.db.fetchrow('''
            SELECT * FROM menu WHERE id = $1
        ''', item_id)

        if row:
            prices = row['price'].split('::')
            variations = row['variations'].split('::')
            return {
                "id": row['id'],
                "name": row['name'],
                "info": row['info'],
                "subinfo": row['subinfo'],
                "price": prices,
                "category": row['category'],
                "variations": variations,
                "image_url": f'{config.main_url}/images/{item_id}.png'
            }
        return None

    async def get_item_category_by_id(self, item_id):
        row = await self.db.fetchrow('''
            SELECT category FROM menu WHERE id = $1
        ''', item_id)
        return row['category'] if row else None

    async def rename_item(self, item_id, new_name):
        await self.db.execute('''
            UPDATE menu SET name = $1 WHERE id = $2
        ''', new_name, item_id)

    async def reinfo_item(self, item_id, new_info):
        await self.db.execute('''
            UPDATE menu SET info = $1 WHERE id = $2
        ''', new_info, item_id)

    async def resubinfo_item(self, item_id, new_subinfo):
        await self.db.execute('''
            UPDATE menu SET subinfo = $1 WHERE id = $2
        ''', new_subinfo, item_id)

    async def get_variations(self, item_id):
        row = await self.db.fetchrow('''
            SELECT variations FROM menu WHERE id = $1
        ''', item_id)
        return row['variations'].split('::') if row else []

    async def revariations_item(self, item_id, new_variations):
        await self.db.execute('''
            UPDATE menu SET variations = $1 WHERE id = $2
        ''', '::'.join(new_variations), item_id)

    async def get_prices(self, item_id):
        row = await self.db.fetchrow('''
            SELECT price FROM menu WHERE id = $1
        ''', item_id)
        return row['price'].split('::') if row else []

    async def reprice_item(self, item_id, new_price):
        await self.db.execute('''
            UPDATE menu SET price = $1 WHERE id = $2
        ''', '::'.join(new_price), item_id)

    async def del_all_items(self, category_id):
        await self.db.execute('''
            DELETE FROM menu WHERE category = $1
        ''', category_id)

    async def add_new_variationprice(self, item_id):
        variations = await self.get_variations(item_id)
        variations.append('Вариация')
        prices = await self.get_prices(item_id)
        prices.append('Цена')
        await self.reprice_item(item_id, prices)
        await self.revariations_item(item_id, variations)

    async def del_last_variationprice(self, item_id):
        variations = await self.get_variations(item_id)
        prices = await self.get_prices(item_id)
        await self.reprice_item(item_id, prices[:-1])
        await self.revariations_item(item_id, variations[:-1])

    async def del_item(self, item_id):
        await self.db.execute('''
            DELETE FROM menu WHERE id = $1
        ''', item_id)

    async def get_all_menu(self):
        categories = await dbs.categories.get_categories()
        result = []
        for category in categories:
            items = await self.get_menu_by_category_id(category["id"])
            result.append({
                "category_id": category["id"],
                "name": category["name"],
                "items": items
            })
        return result

class users:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                                         id SERIAL PRIMARY KEY,
                                         name TEXT,
                                         phone_number INT,
                                         tg_id INT,
                                         tg_first_name TEXT,
                                         tg_last_name TEXT,
                                         tg_username TEXT,
                                         key TEXT,
                                         active_order INT)''')

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
            return dict(row)
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
                "data": eval(order['data']),
                "text": order['text'],
                "delivery_at": order['delivery_at'],
                "comment": order['comment'],
                "order_by": order['order_by'],
                "address": order['address'],
                "status": order['status'],
                "date": order['date'],
                "price": order['price']
            })
        return orders

async def main():
    tg = users()
    await tg.connect('')
    print(await tg.check_tg_connected_by_key('ImZAb2OxCR2rcXCA'))

if __name__ == '__main__':
    asyncio.run(main())
