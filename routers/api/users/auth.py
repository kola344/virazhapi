from fastapi import APIRouter
import db
from models.api.users.auth import auth_phoneModel, auth_get_key_by_phoneModel, get_user_dataModel
from temp.auth_code import auth_codes
import os

router = APIRouter()

@router.post('/auth_user_phone')
async def get_menu_categoriesPage(item: auth_phoneModel):
    '''Возвращает категории меню.'''
    await db.users.auth_user_phone(item.phone)
    return {"status": True, "info": "success"}

@router.post('/get_user_key')
async def get_user_keyPage(item: auth_get_key_by_phoneModel):
    '''Возвращает ключ пользователя для взаимодействия с api по номеру телефона'''
    if item.phone in auth_codes:
        if item.code == auth_codes[item.phone]:
            data = await db.users.get_key_by_phone_number(item.phone)
            return {"status": True, "info": "success", "key": data}
        return {"status": False, "info": "incorrect code", "key": ""}
    return {"status": False, "info": "phone not found", "key": ""}

@router.post('/get_user_data')
async def get_user_dataPage(item: get_user_dataModel):
    '''Возвращает всю информацию о пользователе '''
    data = await db.users.get_user_data_by_key(item.key)
    return {"status": True, "info": 'success', "data": data}


