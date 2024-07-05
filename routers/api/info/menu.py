from fastapi import APIRouter
import db
from models.api.info.menu import get_menu_by_categoryModel
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.post('/get_menu_categories')
async def get_menu_categoriesPage():
    '''Возвращает категории меню.'''

    data = await db.categories.get_categories()
    return {"status": True, "info": "success", "data": data}

@router.post('/get_menu_by_category')
async def get_menu_by_categoryPage(item: get_menu_by_categoryModel):
    '''Возвращает блюда, которые есть в данной категории
        price и variations - связаны с друг другом, оба элемента представляют собой списки
        price = [el1, el2, el3]
        variations = [el1, el2, el3]
        Цена для вариации el1 равна price(el1)
        excample:
        varitaions = ["40см", "Половинка"]
        price = ["800", "450"]
        как должно выглядеть на сайте: цена за 40см = 800, цена за половинку = 450'''
    data = await db.menu.get_menu_by_category_id(category_id=item.category_id)
    return {"status": True, "info": "success", "data": data}

@router.post('/get_all_menu')
async def get_all_menuPage():
    '''Возвращает полное меню'''
    data = await db.menu.get_all_menu()
    return {"status": True, "info": "success", "data": data}