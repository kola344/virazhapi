import asyncio
import config
import db
from virazh_bot.keygen import generate_password, generate_code
from temp.auth_code import auth_codes
import db as dbs
from integration import sms_code
import asyncpg

#TG
class tg_admins:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS tg_admins (
                                     id SERIAL PRIMARY KEY,
                                     user_id BIGINT,
                                     name TEXT)''')

    async def check_admin_by_id(self, admin_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT 1 FROM tg_admins WHERE id = $1''', admin_id)
            return row is not None

    async def check_admin_by_user_id(self, user_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM tg_admins WHERE user_id = $1', user_id)
            return row is not None

    async def add_admin(self, user_id, name):
        if not await self.check_admin_by_user_id(user_id):
            async with self.db.acquire() as connection:
                await connection.execute('''INSERT INTO tg_admins (user_id, name) VALUES ($1, $2)''', user_id, name)

    async def get_admins_list(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT * FROM tg_admins''')
            return [dict(data) for data in cursor]

    async def get_admins_user_ids(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT user_id FROM tg_admins''')
            return [data[0] for data in cursor]

    async def del_admin_by_id(self, admin_id):
        async with self.db.acquire() as connection:
            if await self.check_admin_by_id(admin_id):
                await connection.execute('''DELETE FROM tg_admins WHERE id = $1''', admin_id)

    async def get_admin_user_id_by_id(self, admin_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT user_id FROM tg_admins WHERE id = $1''', admin_id)
            return row["user_id"]

class orders:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS orders (
                                                     id SERIAL PRIMARY KEY,
                                                     data TEXT,
                                                     text TEXT,
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
        async with self.db.acquire() as connection:
            new_id = await connection.fetchval('''
                INSERT INTO orders (data, delivery_at, comment, order_by, address, status, closed, date, price, payment)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING id
            ''', str(data), delivery_at, comment, order_by, address, "🕙 В обработке", 0, date, price, payment)
            return new_id

    async def update_text(self, order_id, text):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE orders SET text = $1 WHERE id = $2
            ''', text, order_id)

    async def update_message_user_id(self, order_id, message_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE orders SET message_user_id = $1 WHERE id = $2
            ''', message_id, order_id)

    async def update_message_id(self, order_id, message_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE orders SET message_id = $1 WHERE id = $2
            ''', message_id, order_id)

    async def set_status(self, status, order_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE orders SET status = $1 WHERE id = $2
            ''', status, order_id)

    async def get_order_data(self, order_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
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
                    "payment": row['payment'],
                    "address": row['address'],
                    "status": row['status'],
                    "message_id": row['message_id'],
                    "closed": row['closed'],
                    "date": row['date'],
                    "price": row['price']
                }
            return None

    async def get_user_message_id(self, order_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT message_user_id FROM orders WHERE id = $1
            ''', order_id)
            return row['message_user_id'] if row else None

    async def get_text(self, order_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT text FROM orders WHERE id = $1
            ''', order_id)
            return row['text'] if row else None

    async def close_order(self, order_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE orders SET closed = $1 WHERE id = $2
            ''', 1, order_id)

    async def get_orders_data_successful(self):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''
                            SELECT * FROM orders ORDER BY id
                        ''')
            return [dict(row) for row in rows if row["status"] == '✅ Заказ выполнен']

class categories:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS categories (
                                             id SERIAL PRIMARY KEY,
                                             name TEXT)''')

    async def check_category_by_name(self, name):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT 1 FROM categories WHERE name = $1
            ''', name)
            return row is not None

    async def check_category_by_id(self, category_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT 1 FROM categories WHERE id = $1
            ''', category_id)
            return row is not None

    async def get_category_by_id(self, category_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT * FROM categories WHERE id = $1
            ''', category_id)
            if row:
                return dict(row)
            return None

    async def get_categories(self):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''
                SELECT * FROM categories ORDER BY id
            ''')
            return [dict(row) for row in rows]

    async def get_categories_with_if(self):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''SELECT DISTINCT categories.id, categories.name FROM categories JOIN menu ON categories.id = menu.category ORDER BY categories.id''')
            return [dict(row) for row in rows]

    async def add_category(self, name):
        async with self.db.acquire() as connection:
            if not await self.check_category_by_name(name):
                new_id = await connection.fetchval('''
                    INSERT INTO categories (name) VALUES ($1)
                    RETURNING id
                ''', name)
                return new_id
            return None

    async def del_category(self, category_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
                DELETE FROM categories WHERE id = $1
            ''', category_id)
            menu_db = dbs.menu
            await menu_db.del_all_items(category_id)

class menu:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS menu (
                                                id SERIAL PRIMARY KEY,
                                                name TEXT,
                                                info TEXT,
                                                subinfo TEXT,
                                                price TEXT,
                                                category INT,
                                                variations TEXT,
                                                image_url TEXT)''')

            await connection.execute('''CREATE TABLE IF NOT EXISTS deactivated_menu (
                                                            id INT,
                                                            name TEXT,
                                                            info TEXT,
                                                            subinfo TEXT,
                                                            price TEXT,
                                                            category INT,
                                                            variations TEXT,
                                                            image_url TEXT)''')

    async def add_deactivated_item(self, item_id, name, info, subinfo, price, category, variations, image_url):
        async with self.db.acquire() as connection:
            new_id = await connection.fetchval('''
                INSERT INTO deactivated_menu (id, name, info, subinfo, price, category, variations, image_url)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id
            ''', item_id, name, info, subinfo,  '::'.join(price), category, '::'.join(variations), image_url)
            return new_id

    async def add_activated_item(self, item_id, name, info, subinfo, price, category, variations, image_url):
        async with self.db.acquire() as connection:
            new_id = await connection.fetchval('''
                INSERT INTO menu (id, name, info, subinfo, price, category, variations, image_url)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id
            ''', item_id, name, info, subinfo, '::'.join(price), category, '::'.join(variations), image_url)
            return new_id

    async def get_deactivated_menu(self):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''
                SELECT * FROM deactivated_menu ORDER BY id
            ''')
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

    async def get_deactivated_item_info_by_id(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT * FROM deactivated_menu WHERE id = $1
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

    async def del_deactivated_item(self, item_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
                DELETE FROM deactivated_menu WHERE id = $1
            ''', item_id)

    async def deactivate(self, item_id):
        item_data = await self.get_item_info_by_id(item_id)
        await self.del_item(item_id)
        await self.add_deactivated_item(item_id, item_data['name'], item_data["info"], item_data["subinfo"], item_data["price"], item_data["category"], item_data["variations"], item_data["image_url"])

    async def activate(self, item_id):
        item_data = await self.get_deactivated_item_info_by_id(item_id)
        await self.del_deactivated_item(item_id)
        await self.add_activated_item(item_id, item_data["name"], item_data["info"], item_data["subinfo"],
                                        item_data["price"],
                                        item_data["category"], item_data["variations"], item_data["image_url"])


    async def get_menu_by_category_id(self, category_id):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''
                SELECT * FROM menu WHERE category = $1 ORDER BY id
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
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''
                SELECT * FROM menu WHERE id = ANY($1::int[]) ORDER BY id
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
        async with self.db.acquire() as connection:
            new_id = await connection.fetchval('''
                INSERT INTO menu (name, price, category, variations)
                VALUES ($1, $2, $3, $4)
                RETURNING id
            ''', 'Позиция', 'Цена', category_id, 'Вариация')
            return new_id

    async def get_item_info_by_id(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
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

    async def check_item_by_id(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM menu WHERE id = $1', item_id)
            return row is not None

    async def get_item_category_by_id(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT category FROM menu WHERE id = $1
            ''', item_id)
            return row['category'] if row else None

    async def rename_item(self, item_id, new_name):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE menu SET name = $1 WHERE id = $2
            ''', new_name, item_id)

    async def reinfo_item(self, item_id, new_info):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE menu SET info = $1 WHERE id = $2
            ''', new_info, item_id)

    async def resubinfo_item(self, item_id, new_subinfo):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE menu SET subinfo = $1 WHERE id = $2
            ''', new_subinfo, item_id)

    async def get_variations(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT variations FROM menu WHERE id = $1
            ''', item_id)
            return row['variations'].split('::') if row else []

    async def revariations_item(self, item_id, new_variations):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE menu SET variations = $1 WHERE id = $2
            ''', '::'.join(new_variations), item_id)

    async def get_prices(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''
                SELECT price FROM menu WHERE id = $1
            ''', item_id)
            return row['price'].split('::') if row else []

    async def reprice_item(self, item_id, new_price):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE menu SET price = $1 WHERE id = $2
            ''', '::'.join(new_price), item_id)

    async def del_all_items(self, category_id):
        async with self.db.acquire() as connection:
            await connection.execute('''
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
        async with self.db.acquire() as connection:
            await connection.execute('''
                DELETE FROM menu WHERE id = $1
            ''', item_id)
    async def del_image(self, item_id):
        async with self.db.acquire() as connection:
            await connection.execute('''DELETE FROM images WHERE item_id = $1''', item_id)

    async def get_all_menu(self):
        categories = await dbs.categories.get_categories_with_if()
        result = []
        for category in categories:
            items = [i for i in await self.get_menu_by_category_id(category["id"]) if i["name"] != "Позиция"]
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

    async def get_users_tg_ids(self):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('SELECT tg_id FROM users')
            return [row['tg_id'] for row in rows if row['tg_id'] is not None]

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS users (
                                             id SERIAL PRIMARY KEY,
                                             name TEXT,
                                             phone_number BIGINT,
                                             tg_id BIGINT,
                                             tg_first_name TEXT,
                                             tg_last_name TEXT,
                                             tg_username TEXT,
                                             key TEXT,
                                             active_order INT)''')

    async def check_user_by_id(self, user_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM users WHERE id = $1', user_id)
            return row is not None

    async def check_user_by_phone_number(self, phone_number):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM users WHERE phone_number = $1', phone_number)
            return row is not None

    async def check_user_by_key(self, key):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM users WHERE key = $1', key)
            return row is not None

    async def auth_user_phone(self, phone_number):
        async with self.db.acquire() as connection:
            if not await self.check_user_by_phone_number(phone_number):
                while True:
                    key = generate_password(16)
                    if not await self.check_user_by_key(key):
                        break
                await connection.execute('INSERT INTO users (phone_number, key) VALUES ($1, $2)', phone_number, key)
            auth_codes[phone_number] = generate_code()
            await sms_code.send_code(phone_number)

    async def get_key_by_phone_number(self, phone_number):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT key FROM users WHERE phone_number = $1', phone_number)
            return row['key'] if row else None

    async def get_phone_by_key(self, key):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT phone_number FROM users WHERE key = $1', key)
            return row['phone_number'] if row else None

    async def get_tg_id_by_phone_number(self, phone_number):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT tg_id FROM users WHERE phone_number = $1', phone_number)
            return row['tg_id'] if row else None

    async def get_user_data_by_key(self, key):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM users WHERE key = $1', key)
            if row:
                return dict(row)
            return None

    async def get_user_active_order_by_key(self, key):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT active_order FROM users WHERE key = $1', key)
            return row['active_order'] if row else None

    async def get_user_tg_id_by_key(self, key):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT tg_id FROM users WHERE key = $1', key)
            return row['tg_id'] if row else None

    async def add_tg_data_with_key(self, key, tg_id, tg_first_name, tg_last_name, tg_username):
        async with self.db.acquire() as connection:
            await connection.execute('''
                UPDATE users
                SET tg_id = $1, tg_first_name = $2, tg_last_name = $3, tg_username = $4
                WHERE key = $5
            ''', tg_id, tg_first_name, tg_last_name, tg_username, key)

    async def check_tg_connected_by_key(self, key):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT tg_id FROM users WHERE key = $1', key)
            return row['tg_id'] is not None if row else False

    async def update_name_by_key(self, key, name):
        async with self.db.acquire() as connection:
            await connection.execute('UPDATE users SET name = $1 WHERE key = $2', name, key)

    async def get_orders_history(self, key):
        async with self.db.acquire() as connection:
            rows = await connection.fetch('SELECT * FROM orders WHERE order_by = $1 ORDER BY id', key)
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
            return orders[::-1]

class images:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS images (
                                                id SERIAL PRIMARY KEY,
                                                item_id INT,
                                                data BYTEA)''')

    async def add_image(self, item_id, data):
        async with self.db.acquire() as connection:
            await connection.execute('''INSERT INTO images (item_id, data) VALUES ($1, $2)''', item_id, data)

    async def get_images(self):
        async with self.db.acquire() as connection:
            cursor = await connection.fetch('''SELECT * FROM images''')
            return [dict(data) for data in cursor]

class text_table:
    def __init__(self):
        self.db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS text_table (
                                                name TEXT,
                                                text TEXT)''')

    async def update_gift(self, text):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM text_table WHERE name = $1', 'gift')
            if row is None:
                await connection.execute('''INSERT INTO text_table (name, text) VALUES ($1, $2)''', 'gift', text)
            else:
                await connection.execute('''
                                UPDATE text_table SET text = $1 WHERE name = $2
                            ''', text, 'gift')

    async def get_gift(self):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM text_table WHERE name = $1', 'gift')
            if row is None:
                return {}
            else:
                item_id = int(row["text"])
                return await db.menu.get_item_info_by_id(item_id)

    async def update_preorder_days(self, text):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM text_table WHERE name = $1', 'preorder_days')
            if row is None:
                await connection.execute('''INSERT INTO text_table (name, text) VALUES ($1, $2)''', 'preorder_days', text)
            else:
                await connection.execute('''
                UPDATE text_table SET text = $1 WHERE name = $2
                ''', text, 'preorder_days')

    async def get_preorder_days(self):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM text_table WHERE name = $1', 'preorder_days')
            if row is None:
                return 0
            else:
                preorder_days = int(row["text"])
                return int(preorder_days)

    async def check_gift(self, item_id):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM text_table WHERE name = $1', 'gift')
            if row is None:
                return False
            else:
                return item_id == int(row["text"])

    async def update_order_text(self, text):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT 1 FROM text_table WHERE name = $1', 'order_text')
            if row is None:
                await connection.execute('''INSERT INTO text_table (name, text) VALUES ($1, $2)''', 'order_text', text)
            else:
                await connection.execute('''
                                UPDATE text_table SET text = $1 WHERE name = $2
                            ''', text, 'order_text')

    async def get_order_text(self):
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM text_table WHERE name = $1', 'order_text')
            if row is None:
                await self.update_order_text('Нет информации')
                return 'Нет информации'
            else:
                return row["text"]

async def main():
    tg = users()
    await tg.connect('')
    print(await tg.check_tg_connected_by_key('ImZAb2OxCR2rcXCA'))

if __name__ == '__main__':
    asyncio.run(main())
