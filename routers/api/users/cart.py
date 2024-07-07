from fastapi import APIRouter
import db
from models.api.users.cart import add_to_cartModel, user_cartModel, delete_from_cartModel
import os
from virazh_bot.functions import order as orders_bot
from datetime import datetime
from routers.api.users import cart_data

router = APIRouter()

@router.post('/add_to_cart')
async def add_to_cartPage(item: add_to_cartModel):
    if not item.user_key in cart_data.carts:
        cart_data.carts[item.user_key] = []
    cart_data.carts[item.user_key].append({"item": item.item_id, "variation": item.variation_id})
    return {"status": True, "info": "success", "cart": cart_data.carts[item.user_key]}

# У меня есть словарь [{"item": 1, "variation": 0}, {"item": 2, "variation": 2}, ...] Как мне удалить элемент, у которого item = 2?

@router.post('/delete_from_cart')
async def delete_from_cartPage(item: delete_from_cartModel):
    cart = cart_data.carts[item.user_key]
    # filtered_cart = [d for d in cart if d["item"] != item.item_id]
    filtered_cart = [elem for i, elem in enumerate(cart) if not (elem["item"] == item.item_id and i == next((j for j, e in enumerate(cart) if e["item"] == item.item_id)))]
    cart_data.carts[item.user_key] = filtered_cart
    return {"status": True, "info": "success", "cart": cart_data.carts[item.user_key]}


@router.post('/get_cart')
async def get_cart_lengthPage(item: user_cartModel):
    print(cart_data.carts)
    if not item.user_key in cart_data.carts:
        return {"status": True, "info": "success", "cart": [], "length": 0}
    return {"status": True, "info": "success", "cart": cart_data.carts[item.user_key], "length": len(cart_data.carts[item.user_key])}

@router.post('/clear_cart')
async def clear_cartPage(item: user_cartModel):
    cart_data.carts[item.user_key] = []
    return {"status": True, "info": "success"}
