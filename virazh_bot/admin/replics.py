from virazh_bot import keygen, temp
import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from virazh_bot.functions.orders_report import report_orders

replic_403 = 'Отказано в доступе'
replic_admin_reg_success = 'Вы были зарегистрированы в как администратор'
replic_admin_menu = 'Панель админа'
replic_admin_cannot_delete_self = 'Вы не можете удалить себя'
replic_admin_adding_new_category_name = 'Добавление новой категории.\nВведите название'
replic_admin_adding_new_category_name_err = 'Ошибка. Введите допустимое название'
replic_admin_menu_editor_rename = 'Введите новое название'
replic_admin_menu_editor_reinfo = 'Введите новое описание'
replic_admin_menu_editor_resubinfo = 'Введите новое субописание'
replic_admin_menu_editor_rephoto = 'Загрузите новое изображение в виде .png'
replic_admin_menu_editor_revariation = 'Введите новую вариацию'
replic_admin_menu_editor_reprice = 'Введите новую цену'
replic_admin_menu_editor_reprice_err = 'Ошибка. Введите правильную цену'
replic_manager_menu = 'Панель менеджера'
replic_update_order_info = 'Введите новую информацию'
replic_help_command = 'Основные команды:\n\n/admin - панель администратора\n\n/manager - панель менеджера\n\n/ads - рекламный кабинет'

def replic_reg_new_admin_keygen():
    temp.reg_admin_key = f'reg_admin_' + keygen.generate_password(12)
    return f'Ссылка на регистрацию нового администратор:\nhttps://t.me/kafevirazh_bot?start={temp.reg_admin_key}'

def replic_reg_new_manager_keygen():
    temp.reg_manager_key = f'reg_manager_' + keygen.generate_password(12)
    return f'Ссылка на регистрацию нового администратора:\nhttps://t.me/kafevirazh_bot?start={temp.reg_manager_key}'

async def replic_menu_admins():
    admins = await db.tg_admin.get_admins_list()
    keyboard = []
    for i in admins:
        keyboard.append([InlineKeyboardButton(text=i['name'], callback_data=f"admin.del.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Управление админами (Нажмите, чтобы удалить)'
    return text, markup

async def replic_menu_categories():
    categories = await db.categories.get_categories()
    keyboard = []
    for i in categories:
        keyboard.append([InlineKeyboardButton(text=i["name"], callback_data=f"admin.category.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'admin.categories.add')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Категории меню'
    return text, markup

async def replic_menu_category(category_id):
    menu = await db.menu.get_menu_by_category_id(category_id)
    keyboard = []
    for i in menu:
        keyboard.append([InlineKeyboardButton(text=i["name"], callback_data=f"admin.menuitem.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data=f'admin.menuadd.{category_id}')])
    keyboard.append([InlineKeyboardButton(text='❌ Удалить', callback_data=f'admin.categorydel.{category_id}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.menu.categories')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Настройки категории'
    return text, markup

def replic_menu_categorydel_confirm(category_id):
    text = 'Внимание, данное действие удалит категорию и все товары в ней\nУдалить?'
    btn1 = InlineKeyboardButton(text='❌ Удалить', callback_data=f'admin.categorydelcon.{category_id}')
    btn2 = InlineKeyboardButton(text='⬅️ Назад', callback_data=f"admin.category.{category_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return text, markup

async def replic_menu_menu_item(item_id, category_id = None):
    data = await db.menu.get_item_info_by_id(item_id)
    if category_id == None:
        category_id = data["category"]
    keyboard = []
    keyboard.append([InlineKeyboardButton(text='Название', callback_data=f'admin.mrename.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='Описание', callback_data=f'admin.mreinfo.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='Субописание', callback_data=f'admin.mresub.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='🖼️ Изображение', callback_data=f'admin.mrei.{item_id}')])
    for i in range(len(data["price"])):
        keyboard.append([InlineKeyboardButton(text=data['variations'][i], callback_data=f'adminrmv.{item_id}.{i}'), InlineKeyboardButton(text=str(data['price'][i]), callback_data=f'adminrmp.{item_id}.{i}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить вариацию', callback_data=f'admin.menuaddv.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='➖ Убрать вариацию', callback_data=f'admin.menudelv.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='❌ Удалить товар', callback_data=f'admin.menudel.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='🔴 Деактивировать', callback_data=f'admin.deactivate.{item_id}')])
    if not await db.text_table.check_gift(item_id):
        keyboard.append([InlineKeyboardButton(text='🎁 Сделать подарком', callback_data=f'admin.gift.{item_id}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.category.{category_id}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'{data["name"]}\n{data["subinfo"]}\n\n{data["info"]}'
    return text, markup

async def replic_deactivated_menu():
    text = 'Деактивированные товары. Нажмите, чтобы активировать'
    menu = await db.menu.get_deactivated_menu()
    keyboard = []
    for i in menu:
        keyboard.append([InlineKeyboardButton(text=i["name"], callback_data=f"admin.activate.{i['id']}")])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin.main.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return text, markup

async def replic_orders_report():
    price, average, count = await report_orders()
    return f'Всего заказов: {count}\nОбщая сумма: {price}\nСредний чек: {average}'
