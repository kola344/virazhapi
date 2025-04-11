from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from virazh_bot.bot_init import bot
from virazh_bot.manager.replics import *
from virazh_bot.manager import keyboards
from virazh_bot.manager.models import edit_preorder_daysModel

import db
import shift_stats_functions

from virazh_bot.bot_logging import log_message
import traceback
router = Router()

@router.message(edit_preorder_daysModel.edit_state, F.text)
async def admin_orderinfoeditFunc(message: Message, state: FSMContext):
    try:
        a = int(message.text)
        await db.text_table.update_preorder_days(message.text)
        text, markup = await replic_preorder_editor_menu()
        await message.answer(text, reply_markup=markup)
        await state.clear()
        await log_message(f'✏️ Новое количество дней предзаказа: {a}')
    except Exception as e:
        traceback.print_exc()
        print(e)
        await message.answer(replic_preorder_days_edit_err)

@router.callback_query(F.data.startswith('manager'))
async def manager_callback(call, state: FSMContext):
    try:
        user_id = call.message.chat.id
        calls = str(call.data).split(sep='.')
        l1 = calls[0]
        l2 = calls[1]
        l3 = calls[2]
        #await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.loading_menu)
        if l2 == 'shift':
            if l3 == 'info':
                text, markup = await replic_shift_info()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l3 == 'true':
                shift_stats_functions.new_stat()
                await log_message('🟢 Смена открыта')
                text, markup = await replic_shift_info()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l3 == 'false':
                times_and_shift.shift = False
                times_and_shift.available_times = []
                await log_message('🔴 Смена закрыта')
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
                await bot.edit_message_text(replic_manager_menu, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.manager_menu)
        elif l2 == 'preorder':
            if l3 == 'menu':
                text, markup = await replic_preorder_editor_menu()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l3 == 'edit':
                await bot.edit_message_text(replic_preorder_days_edit, chat_id=user_id, message_id=call.message.message_id)
                await state.set_state(edit_preorder_daysModel.edit_state)
    except Exception as e:
        traceback.print_exc()
        print(e)

@router.callback_query(F.data.startswith('order'))
async def callback(call):
    try:
        print(call.data)
        user_id = call.message.chat.id
        calls = str(call.data).split(sep='.')
        l1 = calls[0]
        l2 = calls[1]
        l3 = calls[2]
        func = ''
        order_id = 0
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.loading_menu)
        if ':' in l2:
            splited_l2 = l2.split(sep=':')
            func, order_id = splited_l2[0], int(splited_l2[1])
        if func == 'set':
            await db.orders.set_status(config.order_statuses[l3], order_id)
            order_data = await db.orders.get_order_data(order_id)
            user_key = order_data["order_by"]
            user_data = await db.users.get_user_data_by_key(user_key)
            user_tg_id = user_data['tg_id']
            user_tg_username = user_data['tg_username']
            markup, user_markup = await replic_order_manager_markup(l3, order_id, user_tg_id, user_tg_username)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            user_message_id = await db.orders.get_user_message_id(order_id)
            order_text = await db.orders.get_text(order_id)
            try:
                await bot.delete_message(chat_id=user_tg_id, message_id=user_message_id)
                mess = await bot.send_message(chat_id=user_tg_id, text=order_text, reply_markup=user_markup, parse_mode='html')
                await db.orders.update_message_user_id(order_id, mess.message_id)
            except Exception as e:
                try:
                    mess = await bot.send_message(chat_id=user_tg_id, text=order_text, reply_markup=user_markup, parse_mode='html')
                    await db.orders.update_message_user_id(order_id, mess.message_id)
                    markup, user_markup = await replic_order_manager_markup(l3, order_id, user_tg_id, user_tg_username)
                    await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
