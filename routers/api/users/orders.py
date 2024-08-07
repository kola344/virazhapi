from fastapi import APIRouter
import db
from models.api.users.orders import add_orderModel, get_order_historyModel, get_giftModel
import os
from times_and_shift import available_times, shift, get_available_times
from virazh_bot.functions import order as orders_bot
from datetime import datetime
from routers.api.users.cart_data import carts, gift_target

router = APIRouter()

@router.post('/get_orders_history')
async def get_orders_historyPage(item: get_order_historyModel):
    history = await db.users.get_orders_history(item.user_key)
    return {"status": True, "info": "success", "history": history[::-1]}

@router.post('/get_orders_info')
async def get_orders_infoPage():
    text = await db.text_table.get_order_text()
    return {"status": True, "info": "success", "text": text}

@router.get('/get_available_times_delivery')
async def get_available_times_deliveryPage():
    return {"status": True, "info": "success", "available_times": get_available_times('delivery')}

@router.get('/get_available_times_pickup')
async def get_available_times_pickupPage():
    return {"status": True, "info": "success", "available_times": get_available_times('pickup')}

@router.post('/get_gift')
async def get_giftPage(item: get_giftModel):
    if item.user_key in carts:
        price = 0
        for i in carts[item.user_key]:
            try:
                price += int(i["price"])
            except:
                price += 0
        if price >= gift_target:
            return {"status": True, "info": "success", "gift": await db.text_table.get_gift()}
        return {"status": True, "info": "success", "gift": {}}
    return {"status": True, "info": "success", "gift": {}}

@router.post('/add_order')
async def add_orderPage(item: add_orderModel):
    '''Возвращает результат оформления заказа'''
    if carts[item.user_key] == []:
        return {"status": False, "info": "cart is empty", "order_id": ''}
    order_type = 'pickup'
    if item.address != 'Самовывоз':
        order_type = 'delivery'
    if item.delivery_at in get_available_times(order_type):
        await db.users.update_name_by_key(item.user_key, item.name)
        phone_number = await db.users.get_phone_by_key(item.user_key)
        order_subtext = ''
        price = 0
        for i in carts[item.user_key]:
            try:
                price += int(i["price"])
            except:
                price += 0
            order_subtext += f'\n{i["name"]} - {i["variation"]}: {i["price"]}'
        current_date = datetime.now()
        date = current_date.strftime('%d.%m.%Y')
        order_id = await db.orders.add_order(carts[item.user_key], item.delivery_at, item.comment, item.user_key, item.address, date, price, item.payment)
        if price >= gift_target:
            gift_data = await db.text_table.get_gift()
            text = f'ЗАКАЗ #{order_id}{order_subtext}\n🎁{gift_data["name"]}: 0\nИТОГО: {price}\n\nИмя: {item.name}\nАдрес доставки: {item.address}\nДоставить к: {item.delivery_at}\n\nКомментарий к заказу:\n{item.comment}\nОплата: {item.payment}\nНомер: {phone_number}'
        else:
            text = f'ЗАКАЗ #{order_id}{order_subtext}\nИТОГО: {price}\n\nИмя: {item.name}\nАдрес доставки: {item.address}\nДоставить к: {item.delivery_at}\n\nКомментарий к заказу:\n{item.comment}\nОплата: {item.payment}\nНомер: {phone_number}'
        await db.orders.update_text(order_id, text)
        await orders_bot.send_order_to_chat(text, item.user_key, order_id)
        carts[item.user_key] = []
        return {"status": True, "info": "success", "order_id": order_id}
    return {"status": False, "info": 'time is not available', "order_id": ''}
