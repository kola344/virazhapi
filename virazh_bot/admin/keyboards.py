from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Панель админа')]], resize_keyboard=True)
menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Управление админами', callback_data='admin.menu.admins')],
                                             [InlineKeyboardButton(text='Управление меню', callback_data='admin.menu.menu')]])
