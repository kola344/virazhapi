from virazh_bot import keygen, temp
import db
import config
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

replic_403 = 'Отказано в доступе'
replic_admin_reg_success = 'Вы были зарегистрированы в качестве администратора'
replic_admin_menu = 'Панель админа'

def replic_reg_new_admin_keygen():
    temp.reg_admin_key = keygen.generate_password(12)
    return f'Ссылка на регистрацию нового администратра:\n{temp.reg_admin_key}'

async def replic_menu_admins():
    admins = await db.tg_admin.get_admins_list()
    keyboard = []
    for i in admins:
        print(i)
        print(i['name'])
        print(i['id'])
        keyboard.append([InlineKeyboardButton(text=i['name'], callback_data=f"admin.del.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Управление админами (Нажмите, чтобы удалить)'
    return text, markup



