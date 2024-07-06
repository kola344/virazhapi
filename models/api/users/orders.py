from pydantic import BaseModel
from typing import List

class menu_items(BaseModel):
    item_id: int
    variation: int
    price: int

class category_item(BaseModel):
    category_id: int
    items: List[menu_items]


class add_orderModel(BaseModel):
    data: List[category_item]
    delivery_at: str
    comment: str
    user_key: str
    address: str
    name: str