# import asyncio
#
# from virazh_bot import bot
#
# asyncio.run(bot.main())
import requests

print(requests.post('http://127.0.0.1:5500/api/info/menu/get_all_menu').text)