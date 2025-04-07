from pydantic import BaseModel

class get_order_historyModel(BaseModel):
    user_key: str

'''Старая модель данных'''
class send_order_daysModel(BaseModel):
    delivery_at: str
    comment: str
    user_key: str
    address: str
    name: str
    payment: str
    date: str

'''Новая модель данных'''
class add_orderModel(BaseModel):
    delivery_at: str
    comment: str
    user_key: str
    address: str
    name: str
    payment: str
    date: str
    city: str

class get_giftModel(BaseModel):
    user_key: str
    delivery_type: str
