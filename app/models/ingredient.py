from .utils import Model, WithTimestamps

__all__ = ["Ingredient", "IngredientInDish"]


class Ingredient(Model, WithTimestamps):
    name: str


class IngredientInDish(Ingredient):
    quantity: float
    unit: str
