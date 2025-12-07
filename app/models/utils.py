from datetime import datetime

from pydantic import BaseModel


class Model(BaseModel):
    id: int = None


class WithTimestamps(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None
