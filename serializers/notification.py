from pydantic import BaseModel
from datetime import datetime

class NotificationSchema(BaseModel):
    id: int
    restaurant_id: int
    restaurant_name: str
    user_name: str
    rating: int | None = None
    message: str
    created_at: datetime
    read: bool

    class Config:
        from_attributes = True
