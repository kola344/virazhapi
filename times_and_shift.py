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

shift = False
