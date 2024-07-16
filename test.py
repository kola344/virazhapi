import asyncio

from virazh_bot import bot

asyncio.run(bot.main())

# import asyncpg
# import asyncio
# async def run():
#     import db
#     await db.initialize()
#     await db.tg_admin.add_admin(1659397548, 'Коля')
#     print(await db.tg_admin.get_admins_list())
#
# asyncio.run(run())

# import asyncpg
# import asyncio
# async def run():
#     db = await asyncpg.connect(
#         host="82.97.248.66",
#         database="default_db",
#         user="gen_user",
#         password="mGk-base)=-"
#     )
#     await db.execute("DROP TABLE orders")
#
# asyncio.run(run())
# import requests
# print(requests.get('http://127.0.0.1:5500/api/info/menu/get_all_menu').headers)

# import db
# import asyncio
# async def main():
#     await db.initialize()
#     await db.tg_admin.add_admin(5042670643, 'Никита')
#     print(await db.tg_admin.check_admin_by_user_id(5042670643))
#
# asyncio.run(main())


# from locust import HttpUser, TaskSet, task, between
#
# class UserBehavior(TaskSet):
#     @task(1)
#     def index(self):
#         self.client.get("/")
#
# class WebsiteUser(HttpUser):
#     tasks = [UserBehavior]
#     wait_time = between(1, 5)
#     host = "http://cafevirage.vercel.app"  # Укажите ваш URL

# from locust import HttpUser, TaskSet, task, between
#
# class UserBehavior(TaskSet):
#     @task
#     def post_request(self):
#         self.client.post("/api/info/menu/get_all_menu")
#
# class WebsiteUser(HttpUser):
#     tasks = [UserBehavior]
#     wait_time = between(1, 5)
#     host = "http://virazhapi.onrender.com"

# from selenium import webdriver
# import time
#
# url = "http://yourwebsite.com"
#
# driver = webdriver.Chrome()
# start_time = time.time()
# driver.get(url)
# end_time = time.time()
# driver.quit()
#
# print(f"Page Load Time: {end_time - start_time} seconds")