from fastapi import APIRouter
import db
from models.api.users.orders import add_orderModel
import os
from available_times import available_times, shift
from virazh_bot.functions import order as orders_bot
from datetime import datetime

router = APIRouter()

@router.get('/get_available_times')
async def get_available_timesPage():
    return {"status": True, "info": "success", "available_times": available_times}

@router.get('/check_shift')
async def get_shift_status():
    return {"status": True, "info": "success", "shift_status": shift}

@router.post('/add_order')
async def get_menu_categoriesPage(item: add_orderModel):
    '''Возвращает результат оформления заказа'''
    if shift == True:
        if item.delivery_at in available_times:
            await db.users.update_name_by_key(item.user_key, item.name)
            phone_number = await db.users.get_phone_by_key(item.user_key)
            item_ids = []
            items_info = {}
            for i in item.data:
                for j in i.items:
                    item_ids.append(j.item_id)
                    items_info[j.item_id] = j.variation
            data = await db.menu.get_menu_by_item_ids(item_ids)
            order_subtext = ''
            price = 0
            for i in data:
                try:
                    price += int(i["prices"][items_info[i["id"]]])
                except:
                    price = '?'
                order_subtext += f'\n[{i["category"]}] {i["name"]} - {i["variations"][items_info[i["id"]]]}: {i["prices"][items_info[i["id"]]]}'
            current_date = datetime.now()
            date = current_date.strftime('%d.%m.%Y')
            order_id = await db.order.add_order(item.data, item.delivery_at, item.comment, item.user_key, item.address, date, price)
            text = f'ЗАКАЗ #{order_id}{order_subtext}\nИТОГО: {price}\n\nИмя: {item.name}\nАдрес доставки: {item.address}\nДоставикть к: {item.delivery_at}\n\nКомментарий к заказу:\n{item.comment}\nНомер: {phone_number}'
            await orders_bot.send_order_to_chat(text, item.user_key, order_id)
            return {"status": False, "info": "success", "order_id": order_id}
        return {"status": False, "info": 'time is not available', "order_id": ''}
    return {"status": False, "info": "shift is false", "order_id": ""}





