from fastapi import APIRouter
import db
from models.api.users.orders import get_order_historyModel, get_giftModel, send_order_daysModel
from times_and_shift import get_order_times
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

@router.get('/get_order_times')
async def get_order_timesPage():
    return {"status": True, "info": "success", "order_times": await get_order_times()}

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

@router.post('/send_order')
async def send_order_daysPage(item: send_order_daysModel):
    '''Возвращает результат оформления заказа на несколько дней вперед'''
    if carts[item.user_key] == []:
        return {"status": False, "info": "cart is empty", "order_id": ''}
    order_type = 'pickup'
    if item.address != 'Самовывоз':
        order_type = 'delivery'
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
        text = f'ЗАКАЗ #{order_id}{order_subtext}\n🎁{gift_data["name"]}: 0\nИТОГО: {price}\n\nИмя: {item.name}\nАдрес доставки: {item.address}\nДоставить к: {item.date} {item.delivery_at}\n\nКомментарий к заказу:\n{item.comment}\nОплата: {item.payment}\nЭто предзаказ. Доставить {item.date}\nНомер: {phone_number}'
    else:
        text = f'ЗАКАЗ #{order_id}{order_subtext}\nИТОГО: {price}\n\nИмя: {item.name}\nАдрес доставки: {item.address}\nДоставить к: {item.delivery_at}\n\nКомментарий к заказу:\n{item.comment}\nОплата: {item.payment}\nЭто предзаказ. Доставить {item.date}\nНомер: {phone_number}'
    await db.orders.update_text(order_id, text)
    await orders_bot.send_order_to_chat(text, item.user_key, order_id)
    carts[item.user_key] = []
    return {"status": True, "info": "success", "order_id": order_id}
