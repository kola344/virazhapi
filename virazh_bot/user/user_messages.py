import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile

import config
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.user.replics import *
from virazh_bot.user import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
from aiogram.types import ReplyKeyboardRemove

router = Router()

@router.message(models.user_feedbackState.feedback)
async def admin_menueditpriceFunc(message: Message, state: FSMContext):
    order_data = models.user_feedback_data[message.chat.id]
    rate = order_data["rate"]
    order_id = order_data["order_id"]
    await bot.send_message(config.feedback_chat, f'Новый отзыв на заказ #{order_id} - {rate}')
    await message.answer(replic_feedback_sended, reply_markup=ReplyKeyboardRemove())
    await state.clear()
    if message.text != 'Отправить':
        await bot.copy_message(config.feedback_chat, message.chat.id, message_id=message.message_id)



@router.message(F.text.startswith('/start connect_'))
async def start_connect_command(message: Message):
    key = message.text[15:]
    if await db.users.check_user_by_key(key):
        await db.users.add_tg_data_with_key(key, message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        await message.answer(replic_tg_connected)
    else:
        await message.answer(replic_incorrect_key)

@router.callback_query(F.data.startswith('user'))
async def callback(call, state: FSMContext):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    l1 = calls[0]
    l2 = calls[1]
    l3 = calls[2]
    if l2 == 'like':
        models.user_feedback_data[user_id] = {"order_id": int(l3), "rate": "👍"}
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.order_completed)
        await call.message.answer(replic_feedback_to_send_liked, reply_markup=keyboards.feedback)
        await state.set_state(models.user_feedbackState.feedback)
    elif l2 == 'dislike':
        models.user_feedback_data[user_id] = {"order_id": int(l3), "rate": "👎"}
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.order_completed)
        await call.message.answer(replic_feedback_to_send_disliked, reply_markup=keyboards.feedback)
        await state.set_state(models.user_feedbackState.feedback)
