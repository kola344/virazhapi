import times_and_shift
import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import os
from datetime import datetime
import json
from virazh_bot.manager import keyboards
import shift_stats_functions

replic_manager_reg_success = 'Вы были зарегистрированы как менеджер'
replic_403 = 'Отказано в доступе'
replic_manager_menu = 'Панель менеджера'
replic_preorder_days_edit = 'Введите новое значение'
replic_preorder_days_edit_err = 'Введите число'

async def replic_time_info():
    keyboard = []
    for i in times_and_shift.times:
        if i in times_and_shift.available_times:
            keyboard.append([InlineKeyboardButton(text=f'🟢 {i}', callback_data=f'manager.timedel.{i}')])
        else:
            keyboard.append([InlineKeyboardButton(text=f'🔴 {i}', callback_data=f'manager.timeadd.{i}')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'manager.menu.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Доступное время'
    return text, markup

async def replic_shift_info():
    today = datetime.today().strftime('%d.%m.%Y')
    if os.path.exists(f'shift_stats/{today}.json'):
        with open(f'shift_stats/{today}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = f'{today}\nКоличество заказов сегодня: {data["orders_count"]}\nВыполнено: {data["completed_count"]}\nОтменено: {data["cancelled_count"]}\nВыручка сегодня: {data["summ"]}\nСмена: {times_and_shift.shift}'
    else:
        text = f'Нет данных\nСмена: {times_and_shift.shift}'
    if times_and_shift.shift == False:
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Открыть смену', callback_data='manager.shift.true')], [InlineKeyboardButton(text='⬅️ Назад', callback_data='manager.menu.main')]])
        return text, markup
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Закрыть смену', callback_data='manager.shift.false')], [InlineKeyboardButton(text='⬅️ Назад', callback_data='manager.menu.main')]])
    return text, markup

async def replic_order_manager_markup(selected_status, order_id):
    if selected_status == 'completed':
        order_data = await db.orders.get_order_data(order_id)
        shift_stats_functions.add_completed_order('today', order_data["price"])
        markup_user = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Заказ выполнен', callback_data='none')], [InlineKeyboardButton(text='👎', callback_data=f'user.dislike.{order_id}'), InlineKeyboardButton(text='👍', callback_data=f'user.like.{order_id}')]])
        return keyboards.order_completed, markup_user
    elif selected_status == 'cancelled':
        try:
            shift_stats_functions.add_cancelled_order('today')
        except:
            pass
        return keyboards.order_cancelled, keyboards.order_cancelled
    else:
        keyboard = []
        # info_buttons
        keyboard.append([InlineKeyboardButton(text='Статусы', callback_data=f'none')])
        # statuses
        for i in config.order_statuses:
            if i == selected_status:
                keyboard.append([InlineKeyboardButton(text=f'➡️ {config.order_statuses[i]}', callback_data=f'order.set:{order_id}.{i}')])
            else:
                keyboard.append([InlineKeyboardButton(text=config.order_statuses[i], callback_data=f'order.set:{order_id}.{i}')])
        if await db.orders.get_user_message_id(order_id) != None:
            keyboard.append([InlineKeyboardButton(text='🟢 Telegram', callback_data=f'none')])
        else:
            keyboard.append([InlineKeyboardButton(text='🔴 Telegram', callback_data=f'none')])

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        user_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=config.order_statuses[selected_status], callback_data=f'orderr')]])
        return markup, user_markup

async def replic_preorder_editor_menu():
    preorder_days = await db.text_table.get_preorder_days()
    text = f'Текущее количество доступных дней для предзаказа: {preorder_days}'
    return text, keyboards.preorder_menu

