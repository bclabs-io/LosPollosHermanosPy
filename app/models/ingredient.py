from .utils import Model, WithTimestamps


class Ingredient(Model, WithTimestamps):
    name: str


class IngredientInDish(Ingredient):
    quantity: float
    unit: str
