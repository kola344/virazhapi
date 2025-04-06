from pydantic import BaseModel

'''Новая модель данных'''
class addItem_to_cartModel(BaseModel):
    user_key: str
    item_id: int
    variation_id: int
    count: int

class delete_from_cartModel(BaseModel):
    user_key: str
    item_index: int

'''Новая модель данных'''
class itemSubtractAddModel(BaseModel):
    user_key: str
    item_index: int

class user_cartModel(BaseModel):
    user_key: str

class deliveryPriceModel(BaseModel):
    user_key: str
    city: str

class get_influencesModel(BaseModel):
    user_key: str
    delivery_type: str
    city: str
    order_time: str
    current_time: int

class send_promoModel(BaseModel):
    user_key: str
    delivery_type: str
    city: str
    order_time: str
    current_time: str
    promo: str
