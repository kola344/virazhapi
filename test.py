# import asyncio
#
# from virazh_bot import bot
#
# asyncio.run(bot.main())
from datetime import datetime, timedelta

# Текущая дата и время
current_time = datetime.now()

# Минимальное допустимое время для заказа (через час от текущего времени)
min_order_time = current_time + timedelta(hours=1)

# Доступные времена для заказа
available_times = ["14:20", "14:40", "15:00", "15:20", "15:40", "16:00", "17:20", "17:40", "18:00", "18:20", "18:40"]

# Преобразование доступных времен в объекты datetime
available_times_dt = [datetime.strptime(time, "%H:%M") for time in available_times]

# Фильтрация доступных времен, которые больше минимального допустимого времени
filtered_times = [time.strftime("%H:%M") for time in available_times_dt if time.time() > min_order_time.time()]

# Вывод результата
print(filtered_times)