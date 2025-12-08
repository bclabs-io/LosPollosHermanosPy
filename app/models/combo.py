from .dish import Dish
from .utils import Model, WithTimestamps


class Combo(Model, WithTimestamps):
    name: str
    description: str
    total_calories: int = 0
    price: float
    image_url: str

    dishes: list[Dish] = []
