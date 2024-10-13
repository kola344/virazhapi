import asyncio
import traceback

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile

import integration.vk
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.ads.replics import *
from virazh_bot.ads import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
from virazh_bot.functions.orders_report import report_orders
from integration.proxy_api import generate_ad
from virazh_bot.bot_logging import log_message

router = Router()

@router.message(models.AdsStates.item_edit)
async def ads_item_editFunc(message: Message, state: FSMContext):
    user = models.ads_data[message.chat.id]
    if message.text != '⬅️ Назад':
        user.item = message.text
    text, markup = await replic_creator_gpt(user)
    if user.selected["image"]:
        await message.answer_photo(photo=FSInputFile(f'ad_temp/image.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.AdsStates.prompt_edit)
async def ads_prompt_editFunc(message: Message, state: FSMContext):
    user = models.ads_data[message.chat.id]
    if message.text != '⬅️ Назад':
        user.prompt = message.text
    text, markup = await replic_creator_gpt(user)
    if user.selected["image"]:
        await message.answer_photo(photo=FSInputFile(f'ad_temp/image.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.AdsStates.image_edit)
async def ads_image_editFunc(message: Message, state: FSMContext):
    user = models.ads_data[message.chat.id]
    if message.text != '⬅️ Назад':
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path
        await bot.download_file(file_path, f'ad_temp/image.png')
        user.selected["image"] = True
    text, markup = await replic_creator_gpt(user)
    if user.selected["image"]:
        await message.answer_photo(photo=FSInputFile(f'ad_temp/image.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()


@router.message(F.text == '/ads')
async def ads_command(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_menu, reply_markup=keyboards.ads_menu)
    else:
        await message.answer(replic_403)

@router.callback_query(F.data.startswith('ads'))
async def callback(call, state: FSMContext):
    try:
        user_id = call.message.chat.id
        if await db.tg_admin.check_admin_by_user_id(user_id):
            calls = str(call.data).split(sep='.')
            l1 = calls[0]
            l2 = calls[1]
            l3 = calls[2]
            #await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.loading_menu)
            if l2 == 'menu':
                if l3 == 'main':
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=replic_menu, reply_markup=keyboards.ads_menu)
            elif l2 == 'set':
                if l3 == 'chatgpt':
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    text, markup = await replic_gpt_menu()
                    await call.message.answer(text, reply_markup=markup)
                elif l3 == 'vk':
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=replic_vk_no_available)
                    await asyncio.sleep(2)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=replic_menu, reply_markup=keyboards.ads_menu)
            elif l2 == 'create':
                if l3 == 'chatgpt':
                    user = models.AdsSettings()
                    await user.create_item()
                    models.ads_data[user_id] = user
                    text, markup = await replic_creator_gpt(user)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
            elif l2 == 'select':
                if user_id in models.ads_data:
                    if l3 == 'item':
                        await state.set_state(models.AdsStates.item_edit)
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        await call.message.answer(replic_gpt_edit_item, reply_markup=keyboards.gpt_back_to_creator_menu)
                    elif l3 == 'prompt':
                        await state.set_state(models.AdsStates.prompt_edit)
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        await call.message.answer(replic_gpt_edit_prompt, reply_markup=keyboards.gpt_back_to_creator_menu)
                    elif l3 == 'image':
                        await state.set_state(models.AdsStates.image_edit)
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        await call.message.answer(replic_gpt_edit_image, reply_markup=keyboards.gpt_back_to_creator_menu)
                    else:
                        user = models.ads_data[user_id]
                        user.selected[l3] = False if user.selected[l3] else True
                        text, markup = await replic_creator_gpt(user)
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        if user.selected["image"]:
                            await call.message.answer_photo(photo=FSInputFile(f'ad_temp/image.png'), caption=text, reply_markup=markup)
                        else:
                            await call.message.answer(text, reply_markup=markup)
                else:
                    user = models.AdsSettings()
                    await user.create_item()
                    text, markup = await replic_creator_gpt(user)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
            elif l2 == 'gpt':
                if l3 == 'menu':
                    if user_id in models.ads_data:
                        user = models.ads_data[user_id]
                        text, markup = await replic_creator_gpt(user)
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        if user.selected["image"]:
                            await call.message.answer_photo(photo=FSInputFile(f'ad_temp/image.png'), caption=text,reply_markup=markup)
                        else:
                            await call.message.answer(text, reply_markup=markup)
                    else:
                        user = models.AdsSettings()
                        await user.create_item()
                        text, markup = await replic_creator_gpt(user)
                        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
                elif l3 == 'generate':
                    user = models.ads_data[user_id]
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    await call.message.answer(replic_gpt_generation)
                    generated = await generate_ad(user)
                    user.generated = generated
                    if user.selected["image"]:
                        await call.message.answer_photo(photo=FSInputFile(f'ad_temp/image.png'), caption=generated, reply_markup=keyboards.gpt_menu_generated)
                    else:
                        await call.message.answer(generated, reply_markup=keyboards.gpt_menu_generated)
                elif l3 == 'publicate':
                    user = models.ads_data[user_id]
                    await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                    message = await call.message.answer(replic_gpt_publicating)
                    url = await integration.vk.publicate(user.generated, user.selected["image"])
                    text, markup = await replic_gpt_published(url)
                    await bot.edit_message_text(chat_id=user_id, message_id=message.message_id, text=text, reply_markup=markup)
                    await log_message(f"Выложено рекламное объявление:\n{url}")

    except Exception as e:
        traceback.print_exc()
        print(e)