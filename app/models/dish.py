from .ingredient import IngredientInDish
from .utils import Model, WithTimestamps

__all__ = ["Dish"]


class Dish(Model, WithTimestamps):
    name: str
    description: str
    calories: int
    price: float
    image_url: str

    # 關聯屬性
    ingredients: list[IngredientInDish] = []
