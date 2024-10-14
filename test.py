import asyncio

from virazh_bot import bot

# asyncio.run(bot.main())

from datetime import datetime, timedelta

available_times = []

times = ["08:00",
         "08:20", "08:40", "09:00", "09:20", "09:40", "10:00", "10:20", "10:40", "11:00",
         "11:20", "11:40", "12:00", "12:20", "12:40", "13:00",
         "13:20", "13:40", "14:00", "14:20", "14:40", "15:00", "15:20", "15:40",
         "16:00", "16:20", "16:40", "17:00", "17:20", "17:40", "18:00", "18:20",
         "18:40", "19:00", "19:20", "19:40", "20:00", "20:20", "20:40", "21:00"]

remove_times = ["08:00", "08:20", "08:40", "09:00", "09:20", "09:40", "10:00", "10:20", "10:40", "11:00",
                "11:20", "11:40"]

times_oth_days_pickup = ["08:00",
         "08:20", "08:40", "09:00", "09:20", "09:40", "10:00", "10:20", "10:40", "11:00",
         "11:20", "11:40", "12:00", "12:20", "12:40", "13:00",
         "13:20", "13:40", "14:00", "14:20", "14:40", "15:00", "15:20", "15:40",
         "16:00", "16:20", "16:40", "17:00", "17:20", "17:40", "18:00", "18:20",
         "18:40", "19:00", "19:20", "19:40", "20:00", "20:20", "20:40", "21:00"]

times_oth_days_delivery = ["13:00",
         "13:20", "13:40", "14:00", "14:20", "14:40", "15:00", "15:20", "15:40",
         "16:00", "16:20", "16:40", "17:00", "17:20", "17:40", "18:00", "18:20",
         "18:40", "19:00", "19:20", "19:40", "20:00", "20:20", "20:40", "21:00"]

def get_times_oth_days(days):
    # Получаем сегодняшнюю дату
    today = datetime.now() + timedelta(hours=4)

    # Создаем список дат на 3 дня вперед
    future_dates = [today + timedelta(days=i) for i in range(1, 4)]

    # Выводим даты в формате 'YYYY-MM-DD'
    formatted_dates = [{"date": date.strftime('%Y-%m-%d'), "pickup": times_oth_days_pickup, "delivery": times_oth_days_delivery} for date in future_dates]
    return formatted_dates

print(get_times_oth_days(3))

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




# import requests
#
# url = "https://direct.i-dgtl.ru/api/v1/verifier/send"
# headers = {
#     "Authorization": "Basic ODU4ODpvdnlFUEhXMlh0YmFhVmVqZk1mQVI5",
#     "Content-Type": "application/json"
# }
# json = {
#   "gatewayId": "Virazh",
#   "channelType": "SMS",
#   "destination": "79200671561"
# }
#
# print(requests.post(url, headers=headers, json=json).json())