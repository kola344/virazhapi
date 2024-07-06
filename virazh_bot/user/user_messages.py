import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.user.replics import *
from virazh_bot.user import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os

router = Router()

@router.message(F.text.startswith('/start connect_'))
async def start_connect_command(message: Message):
    key = message.text[15:]
    if db.users.check_user_by_key(key):
        await db.users.add_tg_data_with_key(key, message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        await message.answer(replic_tg_connected)
    else:
        await message.answer(replic_incorrect_key)