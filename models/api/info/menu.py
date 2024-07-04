from pydantic import BaseModel

class get_menu_by_categoryModel(BaseModel):
    category_id: int