from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


user_feedback_data = {}
class user_feedbackState(StatesGroup):
    feedback = State()

