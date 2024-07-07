import asyncio
import json

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile

import times_and_shift
import config
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.manager.replics import *
from virazh_bot.manager import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
from datetime import datetime
import shift_stats_functions

router = Router()

@router.callback_query(F.data.startswith('manager'))
async def manager_callback(call):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    l1 = calls[0]
    l2 = calls[1]
    l3 = calls[2]
    if l2 == 'shift':
        if l3 == 'info':
            text, markup = await replic_shift_info()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l3 == 'true':
            shift_stats_functions.new_stat()
            text, markup = await replic_shift_info()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l3 == 'false':
            times_and_shift.shift = False
            times_and_shift.available_times = []
            text, markup = await replic_shift_info()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
    elif l2 == 'time':
        if l3 == 'info':
            text, markup = await replic_time_info()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
    elif l2 == 'timedel':
        times_and_shift.available_times.remove(l3)
        text, markup = await replic_time_info()
        await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
    elif l2 == 'timeadd':
        times_and_shift.available_times.append(l3)
        text, markup = await replic_time_info()
        await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
    elif l2 == 'menu':
        if l3 == 'main':
            await bot.edit_message_text(replic_manager_menu, chat_id=user_id, message_id=call.message.message_id,
                                        reply_markup=keyboards.manager_menu)

@router.callback_query(F.data.startswith('order'))
async def callback(call):
    print(call.data)
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    l1 = calls[0]
    l2 = calls[1]
    l3 = calls[2]
    func = ''
    order_id = 0
    if ':' in l2:
        splited_l2 = l2.split(sep=':')
        func, order_id = splited_l2[0], int(splited_l2[1])
    if func == 'set':
        await db.orders.set_status(config.order_statuses[l3], order_id)
        markup, user_markup = await replic_order_manager_markup(l3, order_id)
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        order_data = await db.orders.get_order_data(order_id)
        user_key = order_data["order_by"]
        user_tg_id = await db.users.get_user_tg_id_by_key(user_key)
        user_message_id = await db.orders.get_user_message_id(order_id)
        order_text = await db.orders.get_text(order_id)
        try:
            await bot.delete_message(chat_id=user_tg_id, message_id=user_message_id)
            mess = await bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            await db.orders.update_message_user_id(order_id, mess.message_id)
            await bot.edit_message_reply_markup(chat_id=user_tg_id, message_id=user_message_id, reply_markup=user_markup)
        except Exception as e:
            print(e)
            try:
                mess = await bot.send_message(chat_id=user_tg_id, text=order_text, reply_markup=user_markup)
                await db.orders.update_message_user_id(order_id, mess.message_id)
                markup, user_markup = await replic_order_manager_markup(l3, order_id)
                await bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            except Exception as e:
                print(e)
