from fastapi import APIRouter
import db
from models.api.users.telegram import check_telegram_connectionModel, get_connetion_urlModel
import os
import config

router = APIRouter()

@router.post('/check_telegram_connection')
async def check_telegram_connectionPage(item: check_telegram_connectionModel):
    '''Возвращает статус подключения клиента к тг'''
    result = await db.users.check_tg_connected_by_key(item.key)
    return {"status": True, "info": "success", "connected": result}

@router.post('/get_conneciton_url')
async def get_connection_urlPage(item: get_connetion_urlModel):
    '''Возвращает ссылку для связки аккаунта клиента с тг'''
    url = f'{config.tg_url}?start=connect_{item.key}'
    return {"status": True, "info": "success", "url": url}


