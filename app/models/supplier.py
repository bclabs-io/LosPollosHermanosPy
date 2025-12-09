from .ingredient import Ingredient
from .utils import Model, WithTimestamps

__all__ = ["SupplierSummary", "Supplier"]


class SupplierSummary(Model):
    name: str
    description: str

    image_url: str = None


class Supplier(SupplierSummary, WithTimestamps):
    contact_person: str
    email: str
    phone: str

    state: str
    city: str
    address: str

    ingredients: list[Ingredient] = []
