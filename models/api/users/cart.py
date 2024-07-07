from pydantic import BaseModel

class add_to_cartModel(BaseModel):
    user_key: str
    item_id: int
    variation_id: int

class delete_from_cartModel(BaseModel):
    user_key: str
    item_id: int

class user_cartModel(BaseModel):
    user_key: str