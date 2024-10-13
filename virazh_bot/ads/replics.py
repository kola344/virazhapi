from virazh_bot import keygen, temp
import db
import config
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import os
from integration import proxy_api
from virazh_bot.ads import keyboards
from virazh_bot.bot_logging import log_message
from virazh_bot.ads.models import AdsSettings

replic_403 = "Отказано в доступе"
replic_menu = "Рекламный кабинет"
replic_gpt_edit_item = 'Введите название товара'
replic_gpt_edit_prompt = 'Введите промпт'
replic_gpt_edit_image = 'Загрузите изображение'
replic_gpt_generation = '✨Генерирую...'
replic_gpt_publicating = '🕙 Публикую...'
replic_vk_no_available = '⚠️ В разработке'

async def replic_gpt_menu():
    balance = await proxy_api.get_balance()
    text = f"✨ Генератор рекламы ChatGPT\n"
    if balance >= 20:
        text += f"💰 Баланс: {balance} руб."
        return text, keyboards.gpt_menu_success
    else:
        text += f"💰 Баланс: {balance} руб.\nВнимание! С балансом менее 20 руб. нельзя создавать рекламные объявления\nПроблема уже отправлена в чат, тех. поддержка решает вопрос"
        await log_message("Баланс ProxyAPI менее 20 руб, невозможно создавать рекламные объявления")
        return text, keyboards.gpt_menu_fail

async def replic_creator_gpt(ad: AdsSettings):
    text = f'Настройка генерации объявления.\nРекламируемый товар: {ad.item}\nПромпт для ChatGPT: {ad.prompt}'
    statuses = ["🔴", "🟢"]
    btn_back = InlineKeyboardButton(text="⬅️ Назад", callback_data="ads.set.chatgpt")
    btn_generate = InlineKeyboardButton(text="✨Сгенерировать", callback_data="ads.gpt.generate")
    btn_date = InlineKeyboardButton(text=f"{statuses[ad.selected['date']]} {ad.date}", callback_data="ads.select.date")
    btn_day_week = InlineKeyboardButton(text=f"{statuses[ad.selected['day_week']]} {ad.day_week}", callback_data="ads.select.day_week")
    btn_season = InlineKeyboardButton(text=f"{statuses[ad.selected['season']]} {ad.season}", callback_data="ads.select.season")
    btn_weather = InlineKeyboardButton(text=f"{statuses[ad.selected['weather']]} {ad.weather}", callback_data="ads.select.weather")
    btn_gift = InlineKeyboardButton(text=f"{statuses[ad.selected['gift']]} {ad.gift}", callback_data="ads.select.gift")
    btn_item = InlineKeyboardButton(text='🍜 Товар', callback_data="ads.select.item")
    btn_prompt = InlineKeyboardButton(text='✏️ Промпт', callback_data="ads.select.prompt")
    btn_image = InlineKeyboardButton(text='🖼️ Изображение', callback_data="ads.select.image")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [btn_date],
        [btn_day_week],
        [btn_season],
        [btn_weather],
        [btn_gift],
        [btn_item],
        [btn_prompt],
        [btn_image],
        [btn_generate],
        [btn_back]
    ])
    return text, markup

async def replic_gpt_published(url):
    text = '✔️ Опубликовано'
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Просмотреть', url=url)]])
    return text, markup
