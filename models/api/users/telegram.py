from pydantic import BaseModel

class check_telegram_connectionModel(BaseModel):
    key: str

class get_connetion_urlModel(BaseModel):
    key: str