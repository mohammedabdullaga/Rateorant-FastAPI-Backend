from pydantic import BaseModel
from datetime import datetime


class FavoriteCreateSchema(BaseModel):
    restaurant_id: int


class FavoriteSchema(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
