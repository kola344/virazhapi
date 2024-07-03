from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.admin.replics import *
from virazh_bot.admin import keyboards
import db

router = Router()

@router.message(F.text.startswith('/start reg_admin_'))
async def start_admin_reg_command(message: Message):
    try:
        key = message.text.split()[1]
        if key == temp.reg_admin_key:
            temp.reg_admin_key = None
            await db.tg_admin.add_admin(message.chat.id, message.from_user.first_name)
            await message.answer(replic_admin_reg_success, reply_markup=keyboards.to_menu)
    except Exception as e:
        print(e)
        await message.answer(replic_403)

@router.message(F.text == '/reg admin')
async def reg_admin_command(message: Message):
    if db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_reg_new_admin_keygen())
    else:
        await message.answer(replic_403)

@router.message(F.text == 'Панель админа')
async def admin_panel(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_admin_menu, reply_markup=keyboards.menu)
    else:
        await message.answer(replic_403)

@router.callback_query(F.data.startswith('admin'))
async def callback(call):
    print(call.data)
    user_id = call.message.chat.id
    if await db.tg_admin.check_admin_by_user_id(user_id):
        calls = str(call.data).split(sep='.')
        l2 = calls[1]
        l3 = calls[2]
        if l2 == 'menu':
            if l3 == 'admins':
                text, markup = await replic_menu_admins()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'main':
            if l3 == 'main':
                await bot.edit_message_text(replic_admin_menu, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.menu)
        elif l2 == 'del':
            await db.tg_admin.del_admin_by_id(int(l3))
            text, markup = await replic_menu_admins()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)

@router.callback_query(F.data)
async def callfasd(call):
    print(call.data)
    print(1)