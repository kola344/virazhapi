import time
import aiosqlite
import asyncio
import config
from virazh_bot.keygen import generate_password, generate_code
from temp.auth_code import auth_codes
import db as dbs

#TG
class tg_admins:
    def __init__(self):
        self.db = None

    async def connect(self, folder='database/'):
        self.db = await aiosqlite.connect(f'{folder}db.db')

    async def check_admin_by_id(self, admin_id):
        cursor = await self.db.execute('SELECT id FROM tg_admins WHERE id = ?', (admin_id,))
        return await cursor.fetchone() is not None

    async def check_admin_by_user_id(self, user_id):
        cursor = await self.db.execute('SELECT user_id FROM tg_admins WHERE user_id = ?', (user_id,))
        return await cursor.fetchone() is not None

    async def add_admin(self, user_id, name):
        if not await self.check_admin_by_user_id(user_id):
            await self.db.execute('INSERT INTO tg_admins (user_id, name) VALUES (?, ?)', (user_id, name))
            await self.db.commit()

    async def get_admins_list(self):
        result = []
        cursor = await self.db.execute('SELECT * FROM tg_admins')
        for admin in await cursor.fetchall():
            result.append({"id": admin[0], "user_id": admin[1], "name": admin[2]})
        return result

    async def get_admins_user_ids(self):
        result = []
        cursor = await self.db.execute('SELECT user_id FROM tg_admins')
        for admin in await cursor.fetchall():
            result.append(admin[0])
        return result

    async def del_admin_by_id(self, admin_id):
        if await self.check_admin_by_id(admin_id):
            await self.db.execute('DELETE FROM tg_admins WHERE id = ?', (admin_id,))
            await self.db.commit()

    async def get_admin_user_id_by_id(self, admin_id):
        cursor = await self.db.execute('SELECT user_id FROM tg_admins WHERE id = ?', (admin_id, ))
        data = await cursor.fetchone()
        return data[0]


class orders:
    def __init__(self):
        self.db = None

    async def connect(self, folder='database/'):
        self.db = await aiosqlite.connect(f'{folder}db.db')

class categories:
    def __init__(self):
        self.db = None

    async def connect(self, folder='database/'):
        self.db = await aiosqlite.connect(f'{folder}db.db')

    async def check_category_by_name(self, name):
        cursor = await self.db.execute('SELECT * FROM categories WHERE name = ?', (name,))
        return await cursor.fetchone() is not None

    async def check_category_by_id(self, category_id):
        cursor = await self.db.execute('SELECT * FROM categories WHERE id = ?', (category_id, ))
        return await cursor.fetchone() is not None

    async def get_category_by_id(self, category_id):
        cursor = await self.db.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        data = await cursor.fetchone()
        return {"id": data[0], "name": data[1], "description": data[2]}

    async def get_categories(self):
        result = []
        cursor = await self.db.execute('SELECT * FROM categories')
        for i in await cursor.fetchall():
            result.append({"id": i[0], "name": i[1]})
        return result

    async def add_category(self, name):
        if not await self.check_category_by_name(name):
            cursor = await self.db.execute('INSERT INTO categories (name) VALUES (?)', (name, ))
            await self.db.commit()
            new_id = cursor.lastrowid
            return new_id

    async def del_category(self, category_id):
        await self.db.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        await self.db.commit()
        menu_db = menu()
        await menu_db.connect()
        await menu_db.del_all_items(category_id)

class menu:
    def __init__(self):
        self.db = None

    async def connect(self, folder='database/'):
        self.db = await aiosqlite.connect(f'{folder}db.db')

    async def get_menu_by_category_id(self, category_id):
        cursor = await self.db.execute("SELECT * FROM menu WHERE category = ?", (category_id, ))
        result = []
        for item in await cursor.fetchall():
            prices = item[4].split('::')
            variations = item[6].split('::')
            result.append({"id": item[0], "name": item[1], "info": item[2], "subinfo": item[3], "price": prices, "category": item[5], "variations": variations, "image_url": f'{config.main_url}/images/{item[0]}.png'})
        return result

    async def add_item(self, category_id):
        cursor = await self.db.execute('INSERT INTO menu (name, price, category, variations) VALUES (?, ?, ?, ?)', ('Позиция', 'Цена', category_id, 'Вариация'))
        await self.db.commit()
        new_id = cursor.lastrowid
        return new_id

    async def get_item_info_by_id(self, item_id):
        cursor = await self.db.execute('SELECT * FROM menu WHERE id = ?', (item_id, ))
        data = await cursor.fetchone()
        prices = data[4].split('::')
        variations = data[6].split('::')
        return {"id": data[0], "name": data[1], "info": data[2], "subinfo": data[3], "price": prices, "category": data[5], "variations": variations, "image_url": f'{config.main_url}/images/{item_id}.png'}

    async def get_item_category_by_id(self, item_id):
        cursor = await self.db.execute('SELECT category FROM menu WHERE id = ?', (item_id,))
        data = await cursor.fetchone()
        return data[0]

    async def rename_item(self, item_id, new_name):
        await self.db.execute('UPDATE menu SET name = ? WHERE id = ?', (new_name, item_id))
        await self.db.commit()

    async def reinfo_item(self, item_id, new_info):
        await self.db.execute('UPDATE menu SET info = ? WHERE id = ?', (new_info, item_id))
        await self.db.commit()

    async def resubinfo_item(self, item_id, new_subinfo):
        await self.db.execute('UPDATE menu SET subinfo = ? WHERE id = ?', (new_subinfo, item_id))
        await self.db.commit()

    async def get_variations(self, item_id):
        cursor = await self.db.execute("SELECT variations FROM menu WHERE id = ?", (item_id,))
        data = await cursor.fetchone()
        return data[0].split('::')

    async def revariations_item(self, item_id, new_variations):
        await self.db.execute('UPDATE menu SET variations = ? WHERE id = ?', ('::'.join(new_variations), item_id))
        await self.db.commit()

    async def get_prices(self, item_id):
        cursor = await self.db.execute("SELECT price FROM menu WHERE id = ?", (item_id,))
        data = await cursor.fetchone()
        return data[0].split('::')

    async def reprice_item(self, item_id, new_price):
        await self.db.execute('UPDATE menu SET price = ? WHERE id = ?', ('::'.join(new_price), item_id))
        await self.db.commit()

    async def del_all_items(self, category_id):
        await self.db.execute('DELETE FROM menu WHERE category = ?', (category_id,))
        await self.db.commit()

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
        await self.db.execute('DELETE FROM menu WHERE id = ?', (item_id,))
        await self.db.commit()

    async def get_all_menu(self):
        categories = await dbs.categories.get_categories()
        result = []
        for category in categories:
            items = await self.get_menu_by_category_id(category["id"])
            result.append({"category_id": category["id"], "name":category["name"], "items": items})
        return result

class users:
    def __init__(self):
        self.db = None

    async def connect(self, folder='database/'):
        self.db = await aiosqlite.connect(f'{folder}db.db')

    async def check_user_by_id(self, user_id):
        cursor = await self.db.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return await cursor.fetchone() is not None

    async def check_user_by_phone_number(self, phone_number):
        cursor = await self.db.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))
        return await cursor.fetchone() is not None

    async def check_user_by_key(self, key):
        cursor = await self.db.execute('SELECT * FROM users WHERE key = ?', (key,))
        return await cursor.fetchone() is not None

    async def auth_user_phone(self, phone_number):
        if not await self.check_user_by_phone_number(phone_number):
            while 1:
                key = generate_password(16)
                if key != self.check_user_by_key(key):
                    break
            await self.db.execute('INSERT INTO users (phone_number, key) VALUES (?, ?)', (phone_number, key))
            await self.db.commit()
        auth_codes[phone_number] = generate_code()

    async def get_key_by_phone_number(self, phone_number):
        cursor = await self.db.execute("SELECT phone_number FROM users WHERE id = ?", (phone_number,))
        data = await cursor.fetchone()
        return data[0]

    async def get_user_data_by_key(self, key):
        cursor = await self.db.execute("SELECT * FROM users WHERE id = ?", (key,))
        data = await cursor.fetchall()
        return {"id": data[0], "name": data[1], "phone_number": data[2], "tg_id": data[3],
                "tg_first_name": data[4], "tg_last_name": data[5],
                "tg_username": data[6], "key": data[7]}

    async def get_user_orders_by_key(self, key):
        pass

    async def get_user_active_order_by_key(self, key):
        pass




async def main():
    tg = tg_admins()
    await tg.connect('')
    print(await tg.add_admin(1659397548, 'Коля'))

if __name__ == '__main__':
    asyncio.run(main())
