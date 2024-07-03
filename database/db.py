import time
import aiosqlite
import asyncio

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


class orders:
    def __init__(self):
        self.db = None

    async def connect(self, folder='database/'):
        self.db = await aiosqlite.connect(f'{folder}db.db')

async def main():
    tg = tg_admins()
    await tg.connect('')
    print(await tg.get_admins_user_ids())

if __name__ == '__main__':
    asyncio.run(main())
