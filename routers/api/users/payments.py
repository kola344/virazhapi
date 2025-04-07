from fastapi import APIRouter
import db
import models.api.users.payments as models

router = APIRouter()

@router.post('/check_paymentMethod')
async def check_paymentMethodPage(item: models.paymentMethodModel):
    return {"status": True, "info": "success", "paymentMethod": await db.paymentMethods.get_method_info_by_key(item.user_key)}

@router.post('/del_paymentMethod')
async def del_paymentMethodPage(item: models.paymentMethodModel):
    await db.paymentMethods.del_payment_method(item.user_key)
    return {"status": True, "info": "success"}

@router.post('/add_paymentMethod')
async def add_paymentMethodPage(item: models.paymentMethodModel):
    #url - URL для привязки. Он потом обратно перекинет в корзину после привязки
    return {"status": True, "info": "success", "url": "testURL"}
