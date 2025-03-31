import db
from routers.api.users import cart_data

async def get_delivery_price(user_key: str, city: str):
    # cart_item = {"item_id", "variation_id", "variation", "price", "name", "info", "subinfo", "count", "total"}
    receipt_amount = 0
    for cart_item in cart_data.carts[user_key]:
        receipt_amount += int(cart_item['total'])
    delivery_price = await db.delivery_price.get_delivery_price_by_city(city, receipt_amount)
    return delivery_price