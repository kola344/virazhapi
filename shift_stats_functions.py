import json
import times_and_shift
from datetime import datetime

def new_stat():
    today = datetime.today().strftime('%d.%m.%Y')
    with open(f'shift_stats/{today}.json', 'w', encoding='utf-8') as f:
        times_and_shift.shift = True
        times_and_shift.available_times = times_and_shift.times.copy()
        json.dump({"orders_count": 0, "completed_count": 0, "cancelled_count": 0, "summ": 0}, f)

def add_completed_order(day = 'today', price = 0):
    if day == 'today':
        today = datetime.today().strftime('%d.%m.%Y')
    with open(f'shift_stats/{today}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data["orders_count"] += 1
        data["completed_count"] += 1
        data["summ"] += price

def add_cancelled_order(day = 'today'):
    today = datetime.today().strftime('%d.%m.%Y')
    with open(f'shift_stats/{today}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data["orders_count"] += 1
        data["cancelled_count"] += 1