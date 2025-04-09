import db
from routers.api.users import cart_data
import bisect
import config

async def calculate_receipt(user_key):
    total = 0
    for i in cart_data.carts[user_key]:
        try:
            total += int(i["total"])
        except:
            total += 0
    return total

async def get_delivery_price(user_key: str, city: str):
    # cart_item = {"item_id", "variation_id", "variation", "price", "name", "info", "subinfo", "count", "total"}
    receipt_amount = await calculate_receipt_with_influences(await calculate_receipt(user_key), user_key)
    delivery_price = await db.delivery_price.get_delivery_price_by_city(city, receipt_amount)
    return delivery_price

async def calculate_delivery(city: str, receipt_amount: int):
    need_delivery_price = await db.delivery_price.calculate_need_delivery_price(city, receipt_amount)
    return need_delivery_price

async def check_promocode(user_key: str, promocode: str):
    #birthdays
    if await db.birthdayPromocodes.check_promocode(promocode):
        if not user_key in cart_data.promocodes:
            cart_data.promocodes[user_key] = []
        cart_data.promocodes[user_key].append({"type": "birthday", "promo": promocode})
        return {"status": True, "info": "success", "promo_data": [
            {"type": "normal", "text": "Промокод в честь дня рождения"},
            {"type": "good", "text": f"Скидка на заказ {cart_data.birthday_discount}% применена"}
            ]}
    return {"status": True, "info": "success", "promo_data": [
        {"type": "critical", "text": "Промокод не существует"}]
            }


async def apply_promocodes(user_key: str):
    if user_key in cart_data.promocodes:
        for promo in cart_data.promocodes[user_key]:
            await db.birthdayPromocodes.update_promocodeStatus(promo['promo'])

async def calculate_receipt_with_influences(total, user_key: str):
    if user_key in cart_data.promocodes:
        for promo in cart_data.promocodes[user_key]:
            if promo['type'] == 'birthday' and await db.birthdayPromocodes.check_promocode(promo['promo']):
                total -= int(total * (cart_data.birthday_discount / 100))
                break
    if user_key in cart_data.influences:
        for influence in cart_data.influences[user_key]:
            if influence['type'] == 'staff':
                total -= int(total * (cart_data.staffs_discount / 100))
                break
    return total

async def str_calculate_receipt_with_influences(total, user_key: str):
    add_text = ''
    if user_key in cart_data.promocodes:
        for promo in cart_data.promocodes[user_key]:
            if promo['type'] == 'birthday' and await db.birthdayPromocodes.check_promocode(promo['promo']):
                discount = int(total * (cart_data.birthday_discount / 100))
                total -= discount
                add_text += f'\n🎉 Скидка в день рождения {cart_data.birthday_discount}%: -{discount}р'
                break
    if user_key in cart_data.influences:
        for influence in cart_data.influences[user_key]:
            if influence['type'] == 'staff':
                discount = int(total * (cart_data.staffs_discount / 100))
                total -= discount
                add_text += f'\n👨‍🍳 Скидка для своих {cart_data.staffs_discount}%: -{discount}р'
                break
    if add_text != '':
        return total, '\n\nСкидки:' + add_text
    return total, ''

async def str_stars(receipt_amount: int, user_key):
    if await db.users.check_tg_connected_by_key(user_key):
        stars_amount = get_stars(receipt_amount)
        if stars_amount:
            user_data = await db.users.get_user_data_by_key(user_key)
            return f'\n\n⭐️Stars - {stars_amount}\nTelegram: <a href="tg://user?id={user_data["tg_id"]}">{user_data["tg_id"]}</a>\nTG_usename: @{user_data["tg_username"]}'
    return ''


async def check_influences(user_key: str, total_amount: int = None):
    phone_number = await db.users.get_phone_by_key(user_key)
    if phone_number in cart_data.staffsPhones:
        is_exists = False
        if user_key in cart_data.influences:
            for influence in cart_data.influences[user_key]:
                if influence['type'] == 'staff':
                    is_exists = True
                    break
        else:
            cart_data.influences[user_key] = []
        if not is_exists:
            cart_data.influences[user_key].append({"type": "staff", "id": -1})


def get_stars(amount: int) -> int:
    idx = bisect.bisect_right(cart_data.receipts_amounts_stars, amount) - 1
    return cart_data.stars_amounts[idx] if idx >= 0 else 0


async def get_influencesList(user_key: str, delivery_type: str, city: str):
    influences = []
    await check_influences(user_key)
    receipt_without_influences = await calculate_receipt(user_key)
    receipt_amount = await calculate_receipt_with_influences(receipt_without_influences, user_key)

    #delivery
    if delivery_type != 'Самовывоз':
        delivery_need = await calculate_delivery(city, receipt_amount)
        if delivery_need:
            influences.append({
                "image": {"exists": False, "url": None, "size": 0},
                "title": {"type": "normal", "data": "Бесплатная доставка"},
                "text": {"type": "normal", "data": f"До бесплатной доставки"},
                "subtext": {"type": "normal", "data": None},
                "price": {"type": "normal", "amount": delivery_need, "isAffects": False},
            })
    #promos
    if user_key in cart_data.promocodes:
        for promo in cart_data.promocodes[user_key]:
            if promo['type'] == 'birthday':
                if await db.birthdayPromocodes.check_promocode(promo['promo']):
                    influences.append({
                        "image": {"exists": False, "url": None, "size": 0},
                        "title": {"type": "normal", "data": "Промокод в честь дня рождения"},
                        "text": {"type": "good", "data": f"Скидка на заказ {cart_data.birthday_discount}% применена!"},
                        "subtext": {"type": "normal", "data": promo['promo']},
                        "price": {"type": "good", "amount": -(receipt_without_influences * (cart_data.birthday_discount / 100)), "isAffects": True}
                    })
                else:
                    influences.append({
                        "image": {"exists": False, "url": None, "size": 0},
                        "title": {"type": "normal", "data": "Промокод в честь дня рождения"},
                        "text": {"type": "warn", "data": f"Закончился срок действия промокода"},
                        "subtext": {"type": "normal", "data": promo['promo']},
                        "price": {"type": "normal", "amount": None, "isAffects": False}
                    })
                break

    #influences
    print(cart_data.influences)
    if user_key in cart_data.influences:
        for influence in cart_data.influences[user_key]:
            if influence['type'] == 'staff':
                influences.append({
                    "image": {"exists": False, "url": None, "size": 0},
                    "title": {"type": "normal", "data": "Скидка для своих"},
                    "text": {"type": "good", "data": f"Применена скидка {cart_data.staffs_discount}%!"},
                    "subtext": {"type": "normal", "data": None},
                    "price": {"type": "good", "amount": -(receipt_without_influences * (cart_data.staffs_discount / 100)), "isAffects": True}
                })

    # stars
    stars_amount = get_stars(receipt_amount)
    if stars_amount:
        if await db.users.check_tg_connected_by_key(user_key):
            influences.append({
                "image": {"exists": True, "url": f"{config.api_url}/icons/telegram.jpeg", "size": 0},
                "title": {"type": "normal", "data": f"Подарок - {stars_amount} Telegram ⭐️Stars!"},
                "text": {"text": "normal", "data": f"После завершения заказа отправим подарок за {stars_amount} ⭐️Stars"},
                "subtext": {"type": "normal", "data": "Не нужны звезды? Укажите в комментарии к заказу ссылку на Telegram другого человека"},
                "price": {"type": "normal", "amount": None, "isAffects": False}
            })
        else:
            influences.append({
                "image": {"exists": True, "url": f"{config.api_url}/icons/telegram.jpeg", "size": 0},
                "title": {"type": "normal", "data": f"Подарок - {stars_amount} Telegram ⭐️Stars!"},
                "text": {"text": "normal",
                         "data": f"Чтобы получить, подключите свой Telegram в профиле после оформления заказа"},
                "subtext": {"type": "normal",
                            "data": "Не нужны звезды? Укажите в комментарии к заказу ссылку на Telegram другого человека"},
                "price": {"type": "normal", "amount": None, "isAffects": False}
            })

    return influences
