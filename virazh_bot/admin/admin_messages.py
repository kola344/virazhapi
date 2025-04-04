import asyncio
import traceback

from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from virazh_bot.bot_init import bot
from virazh_bot.admin.replics import *
from virazh_bot.admin import keyboards, models
import db
from aiogram.fsm.context import FSMContext
import os
from database.db_logging import db_log_message

from integration import vk

import traceback

router = Router()

@router.message(models.deliveryPricesState.deliveryEdit, F.text)
async def deliveryEditFunc(message: Message, state: FSMContext):
    # data = {city, free, price}
    try:
        splited = message.text.split('\n')
        data = []
        for delivery_info in splited:
            info_splited = delivery_info.split('-')
            city, price, free = info_splited[0], int(info_splited[1]), int(info_splited[2])
            data.append({"city": city, "price": price, "free": free})
        await db.delivery_price.delete_from_table()
        await db.delivery_price.update_delivery_price(data)
        text, markup = await replic_deliveryPrices()
        await message.answer(text, reply_markup=markup)
        await state.clear()
    except Exception as e:
        traceback.print_exc()
        await message.answer(replic_editDeliveryPricesErr)


@router.message(models.bsendState.bsend, F.photo)
async def bsendFunc(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    photo_path = 'vkimage.png'
    await bot.download_file(file_path, photo_path)
    user_ids = await vk.get_friends_where_birthday()
    try:
        await vk.send_photo_to_friends(user_ids, photo_path)
        await message.answer(await replic_bsendSended(len(user_ids)))
        await state.clear()
    except:
        await message.answer(replic_bsendErr)
        await state.clear()


@router.message(models.order_info_editorState.edit, F.text)
async def admin_orderinfoeditFunc(message: Message, state: FSMContext):
    await db.text_table.update_order_text(message.text)
    await state.clear()
    await message.answer(message.text, reply_markup=keyboards.order_info_menu)
    await db_log_message('edited_infoOrders', message)

@router.message(models.admin_menu_editorState.price, F.text)
async def admin_menueditpriceFunc(message: Message, state: FSMContext):
    try:
        validate = int(message.text)
        price = message.text
        item = models.admin_menu_data[message.chat.id]
        item_id, price_id = item[0], item[1]
        prices = await db.menu.get_prices(item_id)
        prices[price_id] = price
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
    with open(f'images/{item_id}.png', 'rb') as f:
        await db.images.add_image(item_id, f.read())
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
    await db_log_message('add_category', message)

@router.message(F.text.startswith('/start reg_admin_'))
async def start_admin_reg_command(message: Message):
    try:
        key = message.text.split()[1]
        if key == temp.reg_admin_key:
            temp.reg_admin_key = None
            await db.tg_admin.add_admin(message.chat.id, message.from_user.first_name)
            await message.answer(replic_admin_reg_success, reply_markup=keyboards.to_menu)
            await db_log_message('added_admin', message)
        else:
            await message.answer(replic_403)
    except Exception as e:
        print(e)
        await message.answer(replic_403)

@router.message(F.text == '/help')
async def help_command(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_help_command)
    else:
        await message.answer(replic_403)

@router.message(F.text == '/bsend')
async def bsendCommand(message: Message, state: FSMContext):
    await state.set_state(models.bsendState.bsend)
    await message.answer(replic_bsendPhoto)

@router.message(F.text == '/reg_admin')
async def reg_admin_command(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_reg_new_admin_keygen())
        await db_log_message('add_admin', message, temp.reg_admin_key)
    else:
        await message.answer(replic_403)

@router.message(F.text == '/manager')
async def manager_panel(message: Message):
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_manager_menu, reply_markup=keyboards.manager_menu)
    else:
        await message.answer(replic_403)

@router.message(F.text == '/admin')
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    if await db.tg_admin.check_admin_by_user_id(message.chat.id):
        await message.answer(replic_admin_menu, reply_markup=keyboards.menu)
    else:
        await message.answer(replic_403)

@router.callback_query(models.deliveryPricesState.deliveryEdit, F.data == 'Cancel')
async def deliveryPriceCancelCallback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text, markup = await replic_deliveryPrices()
    await call.message.edit_text(text, reply_markup=markup)

@router.callback_query(F.data == 'admin.editDeliveryPrices')
async def editDeliveryPricesCallback(call: CallbackQuery, state: FSMContext):
    text, markup = await replic_editDeliveryPrices()
    await call.message.edit_text(text, reply_markup=markup)
    await state.set_state(models.deliveryPricesState.deliveryEdit)

@router.callback_query(F.data == 'admin.menu.deliveryprice')
async def deliveryPriceCallback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text, markup = await replic_deliveryPrices()
    await call.message.edit_text(text, reply_markup=markup)

@router.callback_query(F.data.startswith('admin'))
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
                if l3 == 'admins':
                    text, markup = await replic_menu_admins()
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                elif l3 == 'categories':
                    text, markup = await replic_menu_categories()
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                elif l3 == 'deactivated':
                    text, markup = await replic_deactivated_menu()
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                elif l3 == 'orderinfo':
                    text = await db.text_table.get_order_text()
                    await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.order_info_menu)
                elif l3 == 'delivery_report':
                    text = await replic_orders_report()
                    await bot.send_document(chat_id=user_id, document=FSInputFile(f'orders_report.csv'))
                    await bot.send_document(chat_id=user_id, document=FSInputFile(f'orders_report.xlsx'), caption=text)
            elif l2 == 'orderinfo':
                if l3 == 'update':
                    await bot.edit_message_text(replic_update_order_info, chat_id=user_id, message_id=call.message.message_id)
                    await state.set_state(models.order_info_editorState.edit)
            elif l2 == 'deactivate':
                category_id = await db.menu.get_item_category_by_id(int(l3))
                item_data = await db.menu.get_item_info_by_id(int(l3))
                await db.menu.deactivate(int(l3))
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                text, markup = await replic_menu_category(category_id)
                await bot.send_message(text=text, chat_id=user_id, reply_markup=markup)
                await db_log_message('disable_item', call.message, f'- INAME: {item_data["name"]}. IID: {l3}')
            elif l2 == 'activate':
                await db.menu.activate(int(l3))
                item_data = await db.menu.get_item_info_by_id(int(l3))
                text, markup = await replic_deactivated_menu()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                await db_log_message('enable_item', call.message, f'- INAME: {item_data["name"]}. IID: {l3}')
            elif l2 == 'main':
                if l3 == 'main':
                    await bot.edit_message_text(replic_admin_menu, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.menu)
            elif l2 == 'del':
                admin_id = await db.tg_admin.get_admin_user_id_by_id(int(l3))
                if user_id != admin_id:
                    await db.tg_admin.del_admin_by_id(int(l3))
                    await db_log_message('del_admin', call.message, l3)
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
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                text, markup = await replic_menu_category(int(l3))
                await call.message.answer(text, reply_markup=markup)
            elif l2 == 'categorydel':
                text, markup = replic_menu_categorydel_confirm(int(l3))
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l2 == 'categorydelcon':
                category_name = (await db.categories.get_category_by_id(int(l3)))['name']
                await db.categories.del_category(int(l3))
                text, markup = await replic_menu_categories()
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                await db_log_message('del_category', call.message, category_name)
            elif l2 == 'menuadd':
                item_id = await db.menu.add_item(int(l3))
                text, markup = await replic_menu_menu_item(item_id, int(l3))
                await bot.edit_message_text(text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
                await db_log_message('add_item', call.message, f'- CAT: {l3}. IID: {item_id}')
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
                await db.menu.add_new_variationprice(int(l3))
                text, markup = await replic_menu_menu_item(int(l3))
                await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l2 == 'menudelv':
                await db.menu.del_last_variationprice(int(l3))
                text, markup = await replic_menu_menu_item(int(l3))
                await bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
            elif l2 == 'menudel':
                category_id = await db.menu.get_item_category_by_id(int(l3))
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                item_data = await db.menu.get_item_info_by_id(int(l3))
                await db.menu.del_item(int(l3))
                await db.menu.del_image(int(l3))
                text, markup = await replic_menu_category(category_id)
                await call.message.answer(text, reply_markup=markup)
                await db_log_message('del_item', call.message, f"- IID: {l3}. INAME: {item_data['name']}")
            elif l2 == 'gift':
                await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
                await db.text_table.update_gift(l3)
                text, markup = await replic_menu_menu_item(int(l3))
                if os.path.exists(f'images/{l3}.png'):
                    await call.message.answer_photo(photo=FSInputFile(f'images/{l3}.png'), caption=text, reply_markup=markup)
                else:
                    await call.message.answer(text, reply_markup=markup)

    except Exception as e:
        traceback.print_exc()
        print(e)
