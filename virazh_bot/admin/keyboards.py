from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/admin')]], resize_keyboard=True, one_time_keyboard=True)
menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Управление админами', callback_data='admin.menu.admins')],
                                             [InlineKeyboardButton(text='Управление меню', callback_data='admin.menu.categories')],
                                             [InlineKeyboardButton(text='Отключенные товары', callback_data='admin.menu.deactivated')],
                                             [InlineKeyboardButton(text='Информация о заказах', callback_data=f'admin.menu.orderinfo')],
                                             [InlineKeyboardButton(text='Отчет о доставках', callback_data='admin.menu.delivery_report')]])

adding_category_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❌ Отмена')]], resize_keyboard=True)

manager_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Смена', callback_data='manager.shift.info')],
                                                     [InlineKeyboardButton(text='Время', callback_data='manager.time.info')]])

loading_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🕙 Обработка...', callback_data='none')]])

order_info_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Изменить', callback_data='admin.orderinfo.update')], [InlineKeyboardButton(text='⬅️ Назад', callback_data="admin.main.main")]])
