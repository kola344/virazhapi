from virazh_bot.bot_init import bot
import config

async def log_message(message):
    await bot.send_message(config.logs_chat, message)