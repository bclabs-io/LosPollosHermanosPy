from .utils import Model, WithTimestamps


class Image(Model, WithTimestamps):
    id: int
    name: str
    data: bytes
