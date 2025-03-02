import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

replic_addTicket = 'Введите номер своего счастливого билета'
replic_ticketsAddErr = 'Ошибка. Проверьте правильность введенного билета и повторите попытку'

async def replic_tickets(user_id):
    tickets = await db.lucky_tickets.get_user_tickets(user_id)
    keyboard = [
        [InlineKeyboardButton(text=f'{ticket["ticket_id"]}', callback_data=f'ticket.del.{ticket["id"]}')]
        for ticket in tickets
    ]
    keyboard.append([InlineKeyboardButton(text='➕ Добавить билет', callback_data='ticket.add')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='usersMain_menu')])
    text = '🎫 Это меню отслеживания лотереи "Счастливый билет"\n✏️ Если у вас имеются счастливые билеты, то вы можете добавить их сюда, нажав кнопку "➕ Добавить билет".\n📆 8 марта, в 14:00 начнется лотерея в КАФЕ ВИРАЖ. Также будет доступен прямой эфир во ВКонтакте (https://vk.com/virash_kafe_vorsma)\n\n🎁 Если один из ваших билетов выиграет, то мы оповестим вас через этого бота. Информация о том, как забрать приз будет написана в тексте уведомления о выигрыше\n\n✖️ Чтобы удалить Счастливый билет из отслеживания, просто нажмите на него'
    return text, InlineKeyboardMarkup(inline_keyboard=keyboard)