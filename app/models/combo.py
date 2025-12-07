from .dish import Dish
from .utils import Model, WithTimestamps


class Combo(Model, WithTimestamps):
    name: str
    description: str
    price: float
    image_url: str

    dishes: list[Dish] = []
