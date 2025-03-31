from fastapi import APIRouter
import db
from models.api.users.cart import *
from routers.api.users import cart_data
from routers.api.users.functions import get_delivery_price

router = APIRouter()

@router.post('/add_to_cart')
async def add_to_cartPage(item: add_to_cartModel):
    '''Старый метод API'''
    if not item.user_key in cart_data.carts:
        cart_data.carts[item.user_key] = []
    item_data = await db.menu.get_item_info_by_id(item.item_id)
    cart_data.carts[item.user_key].append({"item_id": item.item_id, "variation_id": item.variation_id, "variation": item_data["variations"][item.variation_id], "price": item_data["price"][item.variation_id], "name": item_data["name"], "info": item_data["info"], "subinfo": item_data["subinfo"]})
    return {"status": True, "info": "success"}

@router.post('/addItem_to_cart')
async def addItem_to_cart(item: addItem_to_cartModel):
    '''Новый метод добавления в корзину'''
    if not item.user_key in cart_data.carts:
        cart_data.carts[item.user_key] = []
    item_data = await db.menu.get_item_info_by_id(item.item_id)
    cart_data.carts[item.user_key].append({"item_id": item.item_id, "variation_id": item.variation_id, "variation": item_data["variations"][item.variation_id], "count": item.count, "price": int(item_data["price"][item.variation_id]), "total": int(item_data["price"][item.variation_id]) * item.count, "name": item_data["name"], "info": item_data["info"], "subinfo": item_data["subinfo"]})
    return {"status": True, "info": "success"}

@router.post('/delete_from_cart')
async def delete_from_cartPage(item: delete_from_cartModel):
    # cart = cart_data.carts[item.user_key]
    # filtered_cart = [d for d in cart if d["item"] != item.item_id]
    cart_data.carts[item.user_key].pop(item.item_index)
    return {"status": True, "info": "success"}

@router.post('/subtract_item')
async def subtract_item(item: itemSubtractAddModel):
    '''Вычитает предмет из корзины'''
    count = cart_data.carts[item.user_key][item.item_index]['count'] - 1
    if count <= 0:
        cart_data.carts[item.user_key].pop(item.item_index)
        return {"status": True, "info": "success",
                "itemCount": 0,
                "cart": cart_data.carts[item.user_key]}
    cart_data.carts[item.user_key][item.item_index]['count'] = count
    cart_data.carts[item.user_key][item.item_index]['total'] -= cart_data.carts[item.user_key][item.item_index]['price']
    return {"status": True, "info": "success", "itemCount": cart_data.carts[item.user_key][item.item_index]['count'],
            "cart": cart_data.carts[item.user_key]}

@router.post('/add_item')
async def add_item(item: itemSubtractAddModel):
    '''Прибавляет предмет в корзину'''
    cart_data.carts[item.user_key][item.item_index]['count'] += 1
    cart_data.carts[item.user_key][item.item_index]['total'] += cart_data.carts[item.user_key][item.item_index]['price']
    return {"status": True, "info": "success", "itemCount": cart_data.carts[item.user_key][item.item_index]['count'],
            "cart": cart_data.carts[item.user_key]}

@router.post('/get_cart')
async def get_cart_lengthPage(item: user_cartModel):
    '''Корзина немного изменилась. Теперь у предметов есть "price" - цена за 1, "count" - количество, "total" - общая цена'''
    print(cart_data.carts)
    if not item.user_key in cart_data.carts:
        return {"status": True, "info": "success", "cart": [], "length": 0}
    item_ids = await db.menu.get_item_ids()
    cart = [i for i in cart_data.carts[item.user_key] if i["item_id"] in item_ids]
    return {"status": True, "info": "success", "cart": cart, "length": len(cart)}

@router.post('/clear_cart')
async def clear_cartPage(item: user_cartModel):
    cart_data.carts[item.user_key] = []
    return {"status": True, "info": "success"}

@router.post('/get_delivery_price')
async def get_delivary_pricePage(item: deliveryPriceModel):
    '''Возвращает стоимость доставки'''
    return {"status": True, "info": "success", "delivery_price": await get_delivery_price(item.user_key, item.city)}


@router.post('/get_cities')
async def get_citiesPage():
    '''Возвращает список городов, доступных для доставки'''
    return {"status": True, "info": "success", "cities": await db.delivery_price.get_cities()}
