from datetime import date

from .store import Store
from .utils import Model, WithTimestamps

__all__ = ["Employee"]


class Employee(Model, WithTimestamps):
    name: str
    position: str
    email: str
    phone: str

    hire_date: date
    type_: str

    # 外鍵屬性
    store: Store | None = None
