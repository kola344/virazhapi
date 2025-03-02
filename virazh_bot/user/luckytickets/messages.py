import asyncio
import traceback

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

import config
from virazh_bot.bot_init import bot
from virazh_bot.user.luckytickets.replics import *
from virazh_bot.user.luckytickets import keyboards, models
import db
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(models.admTracking.track, F.text == '/stop')
async def admTrackingFunc(message: Message, state: FSMContext):
    await message.answer('stopped')
    await state.clear()

@router.message(models.admTracking.track)
async def admTrackingFunc(message: Message):
    try:
        splited = message.text.split('$')
        ticket_id = int(splited[0])
        prize = splited[1]
        users = await db.lucky_tickets.get_users_by_ticket(ticket_id)
        for user in users:
            await message.bot.send_message(user['user_id'], f'🎁 Поздравляем!\n🎫 Билет под номером {ticket_id} выигрышный!\n✔️ Ваш приз: {prize}\n\nℹ️ Забрать свой приз вы можете 8 марта с 16:00 в КАФЕ ВИРАЖ в течение всего месяца, показав свой Счастливый билет или показав это уведомление')
            await message.answer(f'User {user["user_id"]} has won')
    except:
        traceback.print_exc()
        await message.answer('Invalid data')

@router.message(F.text == '/admTrack123')
async def admTracking(message: Message, state: FSMContext):
    await state.set_state(models.admTracking.track)
    await message.answer('tracking on')

@router.message(models.user_addTicket.ticketAdd, F.text)
async def addTicketFunc(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if message.text.isdigit() and len(message.text) < 6:
        await message.bot.delete_message(message.chat.id, state_data['message_id'])
        await db.lucky_tickets.add_user_ticket(message.chat.id, int(message.text))
        text, markup = await replic_tickets(message.chat.id)
        await message.answer(text, reply_markup=markup)
        return
    await message.answer(replic_ticketsAddErr)

@router.callback_query(F.data == 'tickets.main.main')
async def tickets(call: CallbackQuery):
    text, markup = await replic_tickets(call.from_user.id)
    await call.message.edit_text(text, reply_markup=markup)

@router.callback_query(models.user_addTicket.ticketAdd, F.data == 'back')
async def ticketsBack(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text, markup = await replic_tickets(call.from_user.id)
    await call.message.edit_text(text, reply_markup=markup)

@router.callback_query(F.data == 'ticket.add')
async def addTicket(call: CallbackQuery, state: FSMContext):
    await state.set_state(models.user_addTicket.ticketAdd)
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text(replic_addTicket, reply_markup=keyboards.to_tickets_menu)

@router.callback_query(F.data.startswith('ticket.del.'))
async def delTicket(call: CallbackQuery):
    track_id = int(call.data.split('.')[2])
    await db.lucky_tickets.del_user_ticket(track_id)
    text, markup = await replic_tickets(call.from_user.id)
    await call.message.edit_text(text, reply_markup=markup)
