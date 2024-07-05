from pydantic import BaseModel

class auth_phoneModel(BaseModel):
    phone: int

class auth_get_key_by_phoneModel(BaseModel):
    phone: int
    code: int

class get_user_dataModel(BaseModel):
    key: str