from datetime import datetime, timedelta

oth_days_count = 3

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
    future_dates = [today + timedelta(days=i) for i in range(1, days)]

    # Выводим даты в формате 'YYYY-MM-DD'
    formatted_dates = [{"date": date.strftime('%d.%m.%Y'), "pickup": times_oth_days_pickup, "delivery": times_oth_days_delivery} for date in future_dates]
    return formatted_dates

def get_available_times(order_type):
    # Текущая дата и время
    current_time = datetime.now()

    # Минимальное допустимое время для заказа (через час от текущего времени)
    min_order_time = current_time + timedelta(hours=4)

    # Преобразование доступных времен в объекты datetime
    available_times_dt = [datetime.strptime(time, "%H:%M") for time in available_times]

    # Фильтрация доступных времен, которые больше минимального допустимого времени
    filtered_times = [time.strftime("%H:%M") for time in available_times_dt if time.time() > min_order_time.time()]
    if order_type == 'delivery':
        for i in remove_times:
            if i in filtered_times:
                filtered_times.remove(i)

    # Вывод результата
    return sorted(filtered_times)

def get_order_times():
    oth_days = get_times_oth_days(oth_days_count)
    today = [{"date": datetime.now().strftime("%d.%m.%Y"), "pickup": get_available_times("pickup"), "delivery": get_available_times("delivery")}]
    return today + oth_days

shift = False