from .ingredient import IngredientInDish
from .utils import Model, WithTimestamps


class Dish(Model, WithTimestamps):
    name: str
    description: str
    calories: int
    price: float
    image_url: str

    ingredients: list[IngredientInDish] = []
