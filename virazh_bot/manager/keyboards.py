from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/manager')]], resize_keyboard=True)
manager_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Смена', callback_data='manager.shift.info')],
                                                     [InlineKeyboardButton(text='Время', callback_data='manager.time.info')],
                                                     [InlineKeyboardButton(text='Дни предзаказа', callback_data='manager.preorder.info')]])
order_cancelled = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Заказ отменен', callback_data='none')]])
order_completed = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Заказ выполнен', callback_data='none')]])

loading_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🕙 Обработка...', callback_data='none')]])
