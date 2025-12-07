from .ingredient import IngredientInDish
from .utils import Model, WithTimestamps


class Dish(Model, WithTimestamps):
    name: str
    image_url: str
    calories: int
    price: float

    ingredients: list[IngredientInDish] = []
