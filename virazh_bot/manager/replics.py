import db
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import config

async def replic_order_manager_markup(selected_status, order_id):
    keyboard = []
    # info_buttons
    keyboard.append([InlineKeyboardButton(text='Статусы', callback_data=f'order')])
    # statuses
    for i in config.order_statuses:
        if i == selected_status:
            keyboard.append([InlineKeyboardButton(text=f'➡️ {config.order_statuses[i]}', callback_data=f'order.set:{order_id}.{i}')])
        else:
            keyboard.append([InlineKeyboardButton(text=config.order_statuses[i], callback_data=f'order.set:{order_id}.{i}')])
    keyboard.append([InlineKeyboardButton(text='Действия', callback_data=f'order')])
    keyboard.append([InlineKeyboardButton(text='❌ Отменить заказ', callback_data=f'order.cancel.{order_id}')])
    keyboard.append([InlineKeyboardButton(text='✔️ Заказ выполнен', callback_data=f'order.complete.{order_id}')])
    if await db.orders.get_user_message_id(order_id) != None:
        print(await db.orders.get_user_message_id(order_id))
        keyboard.append([InlineKeyboardButton(text='🟢 Telegram', callback_data=f'order')])
    else:
        keyboard.append([InlineKeyboardButton(text='🔴 Telegram', callback_data=f'order')])

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    user_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=config.order_statuses[selected_status], callback_data=f'orderr')]])
    return markup, user_markup



