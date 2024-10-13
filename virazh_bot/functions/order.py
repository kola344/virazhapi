from virazh_bot.bot_init import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import db

async def send_order_to_chat(text, user_key, order_id):
    keyboard = []
    #info_buttons
    keyboard.append([InlineKeyboardButton(text='Статусы', callback_data=f'none')])
    #statuses
    for i in config.order_statuses:
        print(i, config.order_statuses[i])
        keyboard.append([InlineKeyboardButton(text=config.order_statuses[i], callback_data=f'order.set:{order_id}.{i}')])

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    message = await bot.send_message(config.orders_chat, text, reply_markup=markup)
    await db.orders.update_message_id(order_id, message.message_id)
    user_id = await db.users.get_user_tg_id_by_key(user_key)
    btn = InlineKeyboardButton(text='🕙 В обработке', callback_data=f'none')
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    try:
        message = await bot.send_message(user_id, text, reply_markup=markup)
        await db.orders.update_message_user_id(order_id, message.message_id)
    except:
        pass

