import db
from routers.api.users import cart_data

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
    receipt_amount = await calculate_receipt_with_influences(user_key)
    delivery_price = await db.delivery_price.get_delivery_price_by_city(city, receipt_amount)
    return delivery_price

async def calculate_delivery(city: str, receipt_amount: int):
    delivery_price = await db.delivery_price.calculate_need_delivery_price(city, receipt_amount)
    return delivery_price

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

async def check_influences(user_key: str):
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

async def get_influencesList(user_key: str, delivery_type: str, city: str):
    influences = []
    await check_influences(user_key)
    receipt_without_influences = await calculate_receipt(user_key)
    receipt_amount = await calculate_receipt_with_influences(receipt_without_influences, user_key)
    print(receipt_without_influences, receipt_amount)
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
    return influences


    # result = [
    #     {
    #         "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 0},
    #         "title": {"type": "normal", "data": "Обычный заголовок"},
    #         "text": {"type": "good", "data": "Плюс что-то"},
    #         "subtext": {"type": "warn", "data": "Внимание на это"},
    #         "price": {"type": "critical", "amount": 120, "isAffects": True},
    #     },
    #     {
    #         "image": {"exists": False, "url": None, "size": 1},
    #         "title": {"type": "critical", "data": "Критично!"},
    #         "text": {"type": "normal", "data": None},
    #         "subtext": {"type": "normal", "data": None},
    #         "price": {"type": "normal", "amount": 100, "isAffects": False},
    #     },
    #     {
    #         "image": {"exists": False, "url": None, "size": 1},
    #         "title": {"type": "normal", "data": None},
    #         "text": {"type": "warn", "data": "Предупреждение"},
    #         "subtext": {"type": "critical", "data": "Серьёзная инфа"},
    #         "price": {"type": "normal", "amount": 10, "isAffects": False},
    #     },
    #     {
    #         "image": {"exists": False, "url": None, "size": 0},
    #         "title": {"type": "normal", "data": None},
    #         "text": {"type": "normal", "data": None},
    #         "subtext": {"type": "normal", "data": None},
    #         "price": {"type": "good", "amount": -15, "isAffects": True},
    #     },
    #     {
    #         "image": {"exists": False, "url": None, "size": 2},
    #         "title": {"type": "good", "data": "Акция!"},
    #         "text": {"type": "good", "data": "Скидка на соус"},
    #         "subtext": {"type": "normal", "data": "Осталось мало времени"},
    #         "price": {"type": "good", "amount": -30, "isAffects": True},
    #     },
    #     {
    #         "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 2},
    #         "title": {"type": "warn", "data": "Обратите внимание"},
    #         "text": {"type": "normal", "data": None},
    #         "subtext": {"type": "normal", "data": None},
    #         "price": {"type": "normal", "amount": None, "isAffects": False},
    #     },
    #     {
    #         "image": {"exists": False, "url": None, "size": 0},
    #         "title": {"type": "normal", "data": None},
    #         "text": {"type": "normal", "data": None},
    #         "subtext": {"type": "normal", "data": None},
    #         "price": {"type": "normal", "amount": 0, "isAffects": False},
    #     },
    #     {
    #         "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 3},
    #         "title": {"type": "critical", "data": "Ошибка системы"},
    #         "text": {"type": "critical", "data": "Сбой в заказе"},
    #         "subtext": {"type": "critical", "data": "Свяжитесь с поддержкой"},
    #         "price": {"type": "critical", "amount": 999, "isAffects": False},
    #     },
    #     {
    #         "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 0},
    #         "title": {"type": "warn", "data": "Осторожно"},
    #         "text": {"type": "warn", "data": "Возможна задержка"},
    #         "subtext": {"type": "warn", "data": "Неопределённая ошибка"},
    #         "price": {"type": "warn", "amount": 20, "isAffects": True},
    #     },
    #     {
    #         "image": {"exists": True, "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": 1},
    #         "title": {"type": "good", "data": "Выгодное предложение"},
    #         "text": {"type": "good", "data": "Соус в подарок"},
    #         "subtext": {"type": "good", "data": "Добавлен автоматически"},
    #         "price": {"type": "good", "amount": -25, "isAffects": True},
    #     },
    #
    #     # Остальные 20 штук — разное сочетание полей
    #     *[
    #         {
    #             "image": {"exists": bool(i % 2), "url": 'https://kola344-virazhapi-4766.twc1.net/images/18.png', "size": i % 4},
    #             "title": {"type": t, "data": f"{t.capitalize()} заголовок" if i % 3 == 0 else None},
    #             "text": {"type": t2, "data": f"{t2.capitalize()} текст" if i % 4 == 0 else None},
    #             "subtext": {"type": t3, "data": f"{t3.capitalize()} подстрока" if i % 5 == 0 else None},
    #             "price": {
    #                 "type": t,
    #                 "amount": (-1) ** (i % 3) * (i * 10),
    #                 "isAffects": choice([True, False])
    #             }
    #         }
    #         for i, (t, t2, t3) in enumerate(zip(
    #             ["normal", "good", "warn", "critical"] * 5,
    #             ["warn", "critical", "normal", "good"] * 5,
    #             ["good", "normal", "critical", "warn"] * 5
    #         ), start=10)
    #     ]
    # ]
    # return result
