from aiogram.fsm.state import State, StatesGroup

user_feedback_data = {}
class user_feedbackState(StatesGroup):
    feedback = State()
