from .dish import Dish
from .utils import Model, WithTimestamps

__all__ = ["Combo"]


class Combo(Model, WithTimestamps):
    name: str
    description: str
    price: float
    image_url: str

    # 關聯屬性
    dishes: list[Dish] = []

    # 推導屬性
    total_calories: int = 0
