from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

feedback = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить')]], resize_keyboard=True)
order_completed = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Заказ выполнен', callback_data='none')]])