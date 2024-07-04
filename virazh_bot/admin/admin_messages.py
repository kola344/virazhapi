import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile
from virazh_bot import temp, keygen
from virazh_bot.bot_init import bot
from virazh_bot.admin.replics import *
from virazh_bot.admin import keyboards, models
import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os

router = Router()

@router.message(models.admin_menu_editorState.price, F.text)
async def admin_menueditpriceFunc(message: Message, state: FSMContext):
    try:
        validate = int(message.text)
        price = message.text
        item = models.admin_menu_data[message.chat.id]
        item_id, price_id = item[0], item[1]
        prices = await db.menu.get_prices(item_id)
        print('прайсы ' + str(prices))
        prices[price_id] = price
        print("+ прайсы" + str(prices))
        await db.menu.reprice_item(item_id, prices)
        text, markup = await replic_menu_menu_item(item_id)
        if os.path.exists(f'images/{item_id}.png'):
            await message.answer_photo(photo=FSInputFile(f'images/{item_id}.png'), caption=text, reply_markup=markup)
        else:
            await message.answer(text, reply_markup=markup)
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer(replic_admin_menu_editor_reprice_err)

@router.message(models.admin_menu_editorState.variation, F.text)
async def admin_menueditvariationFunc(message: Message, state: FSMContext):
    variation = message.text
    item = models.admin_menu_data[message.chat.id]
    item_id, variation_id = item[0], item[1]
    variations = await db.menu.get_variations(item_id)
    variations[variation_id] = variation
    await db.menu.revariations_item(item_id, variations)
    text, markup = await replic_menu_menu_item(item_id)
    if os.path.exists(f'images/{item_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/{item_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()


@router.message(models.admin_menu_editorState.photo, F.photo)
async def admin_menueditphotoFunc(message: Message, state: FSMContext):
    item_id = models.admin_menu_data[message.chat.id]
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, f'images/{item_id}.png')
    text, markup = await replic_menu_menu_item(item_id)
    if os.path.exists(f'images/{item_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/{item_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.admin_menu_editorState.subinfo, F.text)
async def admin_menueditsubinfoFunc(message: Message, state: FSMContext):
    item_id = models.admin_menu_data[message.chat.id]
    await db.menu.resubinfo_item(item_id, message.text)
    text, markup = await replic_menu_menu_item(item_id)
    if os.path.exists(f'images/{item_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/{item_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.admin_menu_editorState.info, F.text)
async def admin_menueditinfoFunc(message: Message, state: FSMContext):
    item_id = models.admin_menu_data[message.chat.id]
    await db.menu.reinfo_item(item_id, message.text)
    text, markup = await replic_menu_menu_item(item_id)
    if os.path.exists(f'images/{item_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/{item_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()


@router.message(models.admin_menu_editorState.name, F.text)
async def admin_menueditnameFunc(message: Message, state: FSMContext):
    item_id = models.admin_menu_data[message.chat.id]
    await db.menu.rename_item(item_id, message.text)
    text, markup = await replic_menu_menu_item(item_id)
    if os.path.exists(f'images/{item_id}.png'):
        await message.answer_photo(photo=FSInputFile(f'images/{item_id}.png'), caption=text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(models.admin_categoryState.add_new_category_name, F.text)
async def admin_addcategoryFunc(message: Message, state: FSMContext):
    category_id = await db.categories.add_category(message.text)
    text, markup = await replic_menu_category(category_id)
    await message.answer(text, reply_markup=markup)
    await state.clear()

@router.message(F.text.startswith('/start reg_admin_'))
async def start_admin_reg_command(message: Message):
    print(message.text)
    print(1)
    try:
        key = message.text.split()[1]
        if key == temp.reg_admin_key:
            temp.reg_admin_key = None
            await db.tg_admin.add_admin(message.chat.id, message.from_user.first_name)
            await message.answer(replic_admin_reg_success, reply_markup=keyboards.to_menu)
        else:
            await message.answer(replic_403)
    except Exception as e:
        print(e)
        await message.answer(replic_403)

@router.message(F.text == '/reg_admin')
async def reg_admin_command(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_reg_new_admin_keygen())
    else:
        await message.answer(replic_403)

@router.message(F.text == '/admin')
async def admin_panel(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_admin_menu, reply_markup=keyboards.menu)
    else:
        await message.answer(replic_403)

@router.callback_query(F.data.startswith('admin'))
async def callback(call, state: FSMContext):
    user_id = call.message.chat.id
    if await db.tg_admin.check_admin_by_user_id(user_id):
        calls = str(call.data).split(sep='.')
        l1 = calls[0]
        l2 = calls[1]
        l3 = calls[2]
        if l2 == 'menu':
            if l3 == 'admins':
                text, markup = await replic_menu_admins()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l3 == 'categories':
                text, markup = await replic_menu_categories()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'main':
            if l3 == 'main':
                await bot.edit_message_text(replic_admin_menu, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.menu)
        elif l2 == 'del':
            admin_id = await db.tg_admin.get_admin_user_id_by_id(int(l3))
            if user_id != admin_id:
                await db.tg_admin.del_admin_by_id(int(l3))
            else:
                await bot.edit_message_text(replic_admin_cannot_delete_self, chat_id=user_id, message_id=call.message.message_id)
                await asyncio.sleep(2)
            text, markup = await replic_menu_admins()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'categories':
            if l3 == 'add':
                await state.set_state(models.admin_categoryState.add_new_category_name)
                await bot.edit_message_text(replic_admin_adding_new_category_name, chat_id=user_id, message_id=call.message.message_id)
        elif l2 == 'category':
            text, markup = await replic_menu_category(int(l3))
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'categorydel':
            text, markup = replic_menu_categorydel_confirm(int(l3))
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'categorydelcon':
            await db.categories.del_category(int(l3))
            text, markup = await replic_menu_categories()
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'menuadd':
            item_id = await db.menu.add_item(int(l3))
            text, markup = await replic_menu_menu_item(item_id, int(l3))
            await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l2 == 'menuitem':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            text, markup = await replic_menu_menu_item(int(l3))
            if os.path.exists(f'images/{l3}.png'):
                await call.message.answer_photo(photo=FSInputFile(f'images/{l3}.png'), caption=text, reply_markup=markup)
            else:
                await call.message.answer(text, reply_markup=markup)
        elif l2 == 'mrename':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            models.admin_menu_data[user_id] = int(l3)
            await state.set_state(models.admin_menu_editorState.name)
            await call.message.answer(replic_admin_menu_editor_rename)
        elif l2 == 'mreinfo':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            models.admin_menu_data[user_id] = int(l3)
            await state.set_state(models.admin_menu_editorState.info)
            await call.message.answer(replic_admin_menu_editor_reinfo)
        elif l2 == 'mresub':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            models.admin_menu_data[user_id] = int(l3)
            await state.set_state(models.admin_menu_editorState.subinfo)
            await call.message.answer(replic_admin_menu_editor_resubinfo)
        elif l2 == 'mrei':
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            models.admin_menu_data[user_id] = int(l3)
            await state.set_state(models.admin_menu_editorState.photo)
            await call.message.answer(replic_admin_menu_editor_rephoto)
        elif 'rmv' in l1:
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            item_id, variation_id = int(l2), int(l3)
            models.admin_menu_data[user_id] = [item_id, variation_id]
            await state.set_state(models.admin_menu_editorState.variation)
            await call.message.answer(replic_admin_menu_editor_revariation)
        elif 'rmp' in l1:
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            item_id, price_id = int(l2), int(l3)
            models.admin_menu_data[user_id] = [item_id, price_id]
            await state.set_state(models.admin_menu_editorState.price)
            await call.message.answer(replic_admin_menu_editor_reprice)
        elif l2 == 'menuaddv':
            # await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await db.menu.add_new_variationprice(int(l3))
            text, markup = await replic_menu_menu_item(int(l3))
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            # if os.path.exists(f'images/{int(l3)}.png'):
            #     await call.message.answer_photo(photo=FSInputFile(f'images/{int(l3)}.png'), caption=text, reply_markup=markup)
            # else:
            #     await call.message.answer(text, reply_markup=markup)
        elif l2 == 'menudelv':
            # await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await db.menu.del_last_variationprice(int(l3))
            text, markup = await replic_menu_menu_item(int(l3))
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            # if os.path.exists(f'images/{int(l3)}.png'):
            #     await call.message.answer_photo(photo=FSInputFile(f'images/{int(l3)}.png'), caption=text,
            #                                     reply_markup=markup)
            # else:
            #     await call.message.answer(text, reply_markup=markup)
        elif l2 == 'menudel':
            category_id = await db.menu.get_item_category_by_id(int(l3))
            await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            await db.menu.del_item(int(l3))
            text, markup = await replic_menu_category(category_id)
            await call.message.answer(text, reply_markup=markup)