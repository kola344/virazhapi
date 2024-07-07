import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile

import config
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.manager.replics import *
from virazh_bot.manager import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os

router = Router()

@router.callback_query(F.data.startswith('admin'))
async def callback(call):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    l1 = calls[0]
    l2 = calls[1]
    l3 = calls[2]
    if l2 == 'fsa':
        pass
    else:
        func = ''
        order_id = 0
        if ':' in l2:
            func, order_id = l2[0], int(l2[1])
        if func == 'set':
            await db.orders.set_status(l3, order_id)
            markup, user_markup = replic_order_manager_markup(l3, order_id)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            try:
                order_data = await db.orders.get_order_data(order_id)
                order_by = order_data["order_by"]
                user_key = order_by["message_user_id"]
                user_message_id = await db.orders.get_user_message_id(order_id)
            except:
                pass