from datetime import time

from .utils import Model, WithTimestamps

__all__ = ["Store"]


class Store(Model, WithTimestamps):
    name: str
    phone: str

    latitude: float
    longitude: float

    state: str
    city: str
    address: str
    zipcode: str

    weekdays: list[int]
    open_time: time
    close_time: time

    # 推導屬性
    employees_count: int = 0
