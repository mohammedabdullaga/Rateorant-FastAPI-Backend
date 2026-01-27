from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreateSchema(BaseModel):
    rating: int = Field(ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None


class ReviewUpdateSchema(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None


class ReviewSchema(BaseModel):
    id: int
    rating: int
    comment: Optional[str] = None
    user_id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewDetailSchema(BaseModel):
    id: int
    rating: int
    comment: Optional[str] = None
    user_id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
