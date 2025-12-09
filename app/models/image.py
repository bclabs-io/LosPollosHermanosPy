from .utils import Model, WithTimestamps

__all__ = ["Image"]


class Image(Model, WithTimestamps):
    id: int
    name: str
    data: bytes
