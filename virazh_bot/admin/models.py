from aiogram.fsm.state import State, StatesGroup

admin_category_data = {}
class admin_category_adding:
    def __init__(self):
        self.category_id = None
        self.category_name = None

class admin_categoryState(StatesGroup):
    add_new_category_name = State()
    delete_category_confirm = State()

admin_menu_data = {}
class admin_menu_editorState(StatesGroup):
    name = State()
    info = State()
    subinfo = State()
    image = State()
    variation = State()
    price = State()
    photo = State()

class order_info_editorState(StatesGroup):
    edit = State()