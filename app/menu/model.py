from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: int
    unit: str
    supplier: str


class Dish(BaseModel):
    id: int
    name: str
    image: str
    calories: int
    price: float
    ingredients: list[Ingredient]


class Combo(BaseModel):
    id: int
    name: str
    image: str
    price: float
    dishes: list[Dish]
