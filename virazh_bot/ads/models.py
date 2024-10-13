from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from config import days_week, seasons
from integration.weather import get_weather
import db

ads_data = {}
#admin: {Дата сегодня, День недели, время года, погода, подарок, блюдо, доп промпт}
class AdsSettings:
    def __init__(self):
        self.date = None
        self.day_week = None
        self.season = None
        self.weather = None
        self.gift = None
        self.item = "Не задано"
        self.prompt = "Не задано"
        self.generated = None

        self.selected = {
            "date": False,
            "day_week": False,
            "season": False,
            "weather": False,
            "gift": False,
            "image": False
        }

    async def create_item(self):
        self.date = datetime.now().strftime("%d.%m.%Y")
        self.day_week = days_week[datetime.now().strftime("%A")]
        self.season = seasons[datetime.now().month - 1]
        self.weather = await get_weather()
        self.gift = (await db.text_table.get_gift())["name"]

class AdsStates(StatesGroup):
    item_edit = State()
    prompt_edit = State()
    image_edit = State()
