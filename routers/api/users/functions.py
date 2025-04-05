import db
from routers.api.users import cart_data

async def get_delivery_price(user_key: str, city: str):
    # cart_item = {"item_id", "variation_id", "variation", "price", "name", "info", "subinfo", "count", "total"}
    receipt_amount = 0
    for cart_item in cart_data.carts[user_key]:
        receipt_amount += int(cart_item['total'])
    delivery_price = await db.delivery_price.get_delivery_price_by_city(city, receipt_amount)
    return delivery_price

'''returns -> List[json]
image: {exists: bool, url: str, size: 0-3} - в size надо заранее на фронте определить размеры картинок, я хз может 0-2 сделать
title: {type: "normal(просто черный текст), good (зеленый), warn(какой-нибудь желтый может), crirtical(красный)", data: str/null} - заголовок делаем жирным
text: {type: "normal, good, warn, critical", data: str/null} - просто обычный текст
subtext: {typ: "normal(серый маленький текст), good (бледно зеленый), warn (бледно желтый), critical(бледный красный)", data: str/null
price: {"type": "normal, good, warn, critical", amount: int, isAffects: bool}'''

from random import choice
def get_influenceList():

    result = [
        {
            "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 0},
            "title": {"type": "normal", "data": "Обычный заголовок"},
            "text": {"type": "good", "data": "Плюс что-то"},
            "subtext": {"type": "warn", "data": "Внимание на это"},
            "price": {"type": "critical", "amount": 120, "isAffects": True},
        },
        {
            "image": {"exists": False, "url": None, "size": 1},
            "title": {"type": "critical", "data": "Критично!"},
            "text": {"type": "normal", "data": None},
            "subtext": {"type": "normal", "data": None},
            "price": {"type": "normal", "amount": 100, "isAffects": False},
        },
        {
            "image": {"exists": False, "url": None, "size": 1},
            "title": {"type": "normal", "data": None},
            "text": {"type": "warn", "data": "Предупреждение"},
            "subtext": {"type": "critical", "data": "Серьёзная инфа"},
            "price": {"type": "normal", "amount": 10, "isAffects": False},
        },
        {
            "image": {"exists": False, "url": None, "size": 0},
            "title": {"type": "normal", "data": None},
            "text": {"type": "normal", "data": None},
            "subtext": {"type": "normal", "data": None},
            "price": {"type": "good", "amount": -15, "isAffects": True},
        },
        {
            "image": {"exists": False, "url": None, "size": 2},
            "title": {"type": "good", "data": "Акция!"},
            "text": {"type": "good", "data": "Скидка на соус"},
            "subtext": {"type": "normal", "data": "Осталось мало времени"},
            "price": {"type": "good", "amount": -30, "isAffects": True},
        },
        {
            "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 2},
            "title": {"type": "warn", "data": "Обратите внимание"},
            "text": {"type": "normal", "data": None},
            "subtext": {"type": "normal", "data": None},
            "price": {"type": "normal", "amount": None, "isAffects": False},
        },
        {
            "image": {"exists": False, "url": None, "size": 0},
            "title": {"type": "normal", "data": None},
            "text": {"type": "normal", "data": None},
            "subtext": {"type": "normal", "data": None},
            "price": {"type": "normal", "amount": 0, "isAffects": False},
        },
        {
            "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 3},
            "title": {"type": "critical", "data": "Ошибка системы"},
            "text": {"type": "critical", "data": "Сбой в заказе"},
            "subtext": {"type": "critical", "data": "Свяжитесь с поддержкой"},
            "price": {"type": "critical", "amount": 999, "isAffects": False},
        },
        {
            "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 0},
            "title": {"type": "warn", "data": "Осторожно"},
            "text": {"type": "warn", "data": "Возможна задержка"},
            "subtext": {"type": "warn", "data": "Неопределённая ошибка"},
            "price": {"type": "warn", "amount": 20, "isAffects": True},
        },
        {
            "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 1},
            "title": {"type": "good", "data": "Выгодное предложение"},
            "text": {"type": "good", "data": "Соус в подарок"},
            "subtext": {"type": "good", "data": "Добавлен автоматически"},
            "price": {"type": "good", "amount": -25, "isAffects": True},
        },

        # Остальные 20 штук — разное сочетание полей
        *[
            {
                "image": {"exists": bool(i % 2), "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": i % 4},
                "title": {"type": t, "data": f"{t.capitalize()} заголовок" if i % 3 == 0 else None},
                "text": {"type": t2, "data": f"{t2.capitalize()} текст" if i % 4 == 0 else None},
                "subtext": {"type": t3, "data": f"{t3.capitalize()} подстрока" if i % 5 == 0 else None},
                "price": {
                    "type": t,
                    "amount": (-1) ** (i % 3) * (i * 10),
                    "isAffects": choice([True, False])
                }
            }
            for i, (t, t2, t3) in enumerate(zip(
                ["normal", "good", "warn", "critical"] * 5,
                ["warn", "critical", "normal", "good"] * 5,
                ["good", "normal", "critical", "warn"] * 5
            ), start=10)
        ]
    ]
    return result
