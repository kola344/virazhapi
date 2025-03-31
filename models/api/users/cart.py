from pydantic import BaseModel

'''Старая модель данных'''
class add_to_cartModel(BaseModel):
    user_key: str
    item_id: int
    variation_id: int

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
