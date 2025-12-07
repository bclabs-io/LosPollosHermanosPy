from .dish import Dish
from .utils import Model, WithTimestamps


class Combo(Model, WithTimestamps):
    name: str
    image_url: str
    price: float

    dishes: list[Dish] = []
