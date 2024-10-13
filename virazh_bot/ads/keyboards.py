from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

loading_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🕙 Обработка...', callback_data='none')]])

ads_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ChatGPT", callback_data="ads.set.chatgpt")],
    [InlineKeyboardButton(text="VK", callback_data="ads.set.vk")]
])

gpt_menu_success = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать объявление", callback_data="ads.create.chatgpt")],
     [InlineKeyboardButton(text="⬅️ Назад", callback_data="ads.menu.main")]
])

gpt_menu_fail = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="ads.menu.main")]
])

gpt_menu_generated = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➡️ Выложить объявление", callback_data="ads.gpt.publicate")],
    [InlineKeyboardButton(text="🔄 Перегенерировать", callback_data="ads.gpt.generate")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="ads.gpt.menu")]
])

gpt_back_to_creator_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад")]], one_time_keyboard=True, resize_keyboard=True)
