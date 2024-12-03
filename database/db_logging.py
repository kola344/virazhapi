from virazh_bot.bot_init import bot
import config
from aiogram.types import Message

async def db_log_message(log_type, message: Message, current_data = None):
    message_text = 'LOGGING\n'
    if log_type == 'add_category':
        message_text += f'➕ ADD: CATEGORY\nCATEGORY NAME: {message.text}'
    elif log_type == 'del_category':
        message_text += f'❌ DEL: CATEGORY\nCATEGORY NAME: {current_data}'
    elif log_type == 'add_item':
        message_text += f'✔️ ADD: ITEM\nITEM: {current_data}'
    elif log_type == 'del_item':
        message_text += f'❌ DEL: ITEM\nITEM: {current_data}'
    elif log_type == 'edited_infoOrders':
        message_text += f'✏️ EDIT: INFO ORDERS\nNEW ORDER INFO: {message.text}'
    elif log_type == 'disable_item':
        message_text += f'🟡 DISABLE: ITEM\nITEM: {current_data}'
    elif log_type == 'enable_item':
        message_text += f'🟢 ENABLE: ITEM\nITEM: {current_data}'
    elif log_type == 'add_admin':
        message_text += f'➕ ADD: ADMIN\nADMIN KEY: {current_data}'
    elif log_type == 'added_admin':
        message_text += '✅ ADDED: ADMIN'
    elif log_type == 'del_admin':
        message_text += f'❌ DEL: ADMIN\nADMIN ID: {current_data}'
    message_text += f'\n\nBY: id{message.chat.id} - {message.chat.first_name} {message.chat.last_name} (@{message.chat.username})'
    await bot.send_message(config.db_logs_chat, message_text)