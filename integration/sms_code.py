import config
from integration import notisend
from virazh_bot.bot_init import bot
import db
from temp.auth_code import auth_codes

from virazh_bot.bot_init import bot

async def send_code(phone_number):
    await bot.send_message(-4253301518, f'Код подтверждения: {auth_codes[phone_number]}.')
    # try:
    #     tg_id = await db.users.get_tg_id_by_phone_number(phone_number)
    #     await bot.send_message(tg_id, f'Ваш код: {auth_codes[phone_number]}')
    # except Exception as e:
    #     print(e)
    #     sms = notisend.SMS(config.notisend_project, config.notisend_api_key)
    #     await sms.sendSMS(str(phone_number), f"КАФЕ ВИРАЖ. Код: {auth_codes[phone_number]}")