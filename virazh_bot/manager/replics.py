import db
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import config

def replic_order_manager_markup(selected_status, order_id):
    keyboard = []
    # info_buttons
    keyboard.append([InlineKeyboardButton(text='Статусы', callback_data=f'order')])
    # statuses
    btns_status = []
    for i in config.order_statuses:
        if i == selected_status:
            btns_status.append([InlineKeyboardButton(text=f'➡️ {config.order_statuses[i]}', callback_data=f'order.set:{order_id}.{i}')])
        else:
            btns_status.append([InlineKeyboardButton(text=config.order_statuses[i], callback_data=f'order.set:{order_id}.{i}')])
    keyboard.append([InlineKeyboardButton(text='Действия', callback_data=f'order')])
    keyboard.append([InlineKeyboardButton(text='❌ Отменить заказ', callback_data=f'order.cancel.{order_id}')])
    keyboard.append([InlineKeyboardButton(text='✔️ Заказ выполнен', callback_data=f'order.complete.{order_id}')])

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    user_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=config.order_statuses[selected_status], callback_data=f'order')]])
    return markup, user_markup



