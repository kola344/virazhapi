from virazh_bot.bot_init import bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import config
import db

async def send_order_to_chat(text, user_key, order_id):
    #info_buttons
    btn_statuses = InlineKeyboardButton(text='Статусы', callback_data=f'order')
    btn_other = InlineKeyboardButton(text='Действия', callback_data=f'order')
    btn_time = InlineKeyboardButton(text='Время', callback_data=f'order')
    #statuses
    btn_accept = InlineKeyboardButton(text='✅ Принят', callback_data=f'order.set:{order_id}.1')
    btn_on_kitchen = InlineKeyboardButton(text='🧑‍🍳 На кухне', callback_data=f'order.set:{order_id}.2')
    btn_ready_to_delivery = InlineKeyboardButton(text='📦 Готов к отправке', callback_data=f'order.set:{order_id}.3')
    btn_in_delivery = InlineKeyboardButton(text='🚚 В пути', callback_data=f'order.set:{order_id}.4')
    btn_delivered = InlineKeyboardButton(text='📬 Доставлено', callback_data=f'order.set:{order_id}.5')
    btn_available_to_pickup = InlineKeyboardButton(text='🏢 Можно забрать самовывоз', callback_data=f'order.set:{order_id}.6')
    btn_order_cancelled = InlineKeyboardButton(text='❌ Отменить заказ', callback_data=f'order.cancel.{order_id}')
    btn_order_completed = InlineKeyboardButton(text='✔️ Заказ выполнен', callback_data=f'order.complete.{order_id}')

    markup = InlineKeyboardMarkup(inline_keyboard=[[btn_statuses], [btn_accept], [btn_on_kitchen],
                                                   [btn_ready_to_delivery], [btn_in_delivery], [btn_delivered],
                                                   [btn_available_to_pickup], [btn_other], [btn_order_cancelled],
                                                   [btn_order_completed]])

    message = await bot.send_message(config.orders_chat, text, reply_markup=markup)
    await db.orders.update_message_id(order_id, message.message_id)
    user_id = await db.users.get_user_tg_id_by_key(user_key)
    btn = InlineKeyboardButton(text='🕙 В обработке')
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    message = await bot.send_message(user_id, text)
    await db.order.update_message_user_id(order_id, message.message_id)

