from fastapi import APIRouter
import db
from models.api.users.orders import add_orderModel, get_order_historyModel
import os
from times_and_shift import available_times, shift, get_available_times
from virazh_bot.functions import order as orders_bot
from datetime import datetime
from routers.api.users.cart_data import carts

router = APIRouter()

@router.post('/get_orders_history')
async def get_orders_history(item: get_order_historyModel):
    history = await db.users.get_orders_history(item.user_key)
    return {"status": True, "info": "success", "history": history}

@router.get('/get_available_times')
async def get_available_timesPage():
    return {"status": True, "info": "success", "available_times": get_available_times()}

@router.post('/add_order')
async def get_menu_categoriesPage(item: add_orderModel):
    '''Возвращает результат оформления заказа'''
    if item.delivery_at in available_times:
        await db.users.update_name_by_key(item.user_key, item.name)
        phone_number = await db.users.get_phone_by_key(item.user_key)
        item_ids = []
        items_info = {}
        for i in carts[item.user_key]:
            item_ids.append(i["item"])
            items_info[i["item"]] = i["variation"]
        data = await db.menu.get_menu_by_item_ids(item_ids)
        order_subtext = ''
        price = 0
        for i in data:
            try:
                price += int(i["prices"][items_info[i["id"]]])
            except:
                price = '?'
            order_subtext += f'\n{i["name"]} - {i["variations"][items_info[i["id"]]]}: {i["prices"][items_info[i["id"]]]}'
        current_date = datetime.now()
        date = current_date.strftime('%d.%m.%Y')
        order_id = await db.orders.add_order(carts[item.user_key], item.delivery_at, item.comment, item.user_key, item.address, date, price)
        text = f'ЗАКАЗ #{order_id}{order_subtext}\nИТОГО: {price}\n\nИмя: {item.name}\nАдрес доставки: {item.address}\nДоставикть к: {item.delivery_at}\n\nКомментарий к заказу:\n{item.comment}\nНомер: {phone_number}'
        await db.orders.update_text(order_id, text)
        await orders_bot.send_order_to_chat(text, item.user_key, order_id)
        carts[item.user_key] = []
        return {"status": True, "info": "success", "order_id": order_id}
    return {"status": False, "info": 'time is not available', "order_id": ''}
