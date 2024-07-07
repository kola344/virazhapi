from pydantic import BaseModel
from typing import List

class get_order_historyModel(BaseModel):
    user_key: str

class add_orderModel(BaseModel):
    delivery_at: str
    comment: str
    user_key: str
    address: str
    name: str

