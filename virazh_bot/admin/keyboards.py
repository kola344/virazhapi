from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/admin')]], resize_keyboard=True, one_time_keyboard=True)
menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Управление админами', callback_data='admin.menu.admins')],
                                             [InlineKeyboardButton(text='Управление меню', callback_data='admin.menu.categories')]])

adding_category_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❌ Отмена')]], resize_keyboard=True)

manager_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Смена', callback_data='manager.shift.info')],
                                                     [InlineKeyboardButton(text='Время', callback_data='manager.time.info')]])