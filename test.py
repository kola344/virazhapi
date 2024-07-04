# import asyncio
#
# from virazh_bot import bot
#
# asyncio.run(bot.main())
import requests

categories = requests.post('http://127.0.0.1:5500/api/info/menu/get_menu_categories').json()["data"]
for i in categories:
    json = {"category_id": i["id"]}
    print(requests.post('http://127.0.0.1:5500/api/info/menu/get_menu_by_category', json=json).json())