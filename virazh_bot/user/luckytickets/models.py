from aiogram.fsm.state import State, StatesGroup

class user_addTicket(StatesGroup):
    ticketAdd = State()

class admTracking(StatesGroup):
    track = State()
