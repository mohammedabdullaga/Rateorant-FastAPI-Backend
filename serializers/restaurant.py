from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CategorySchema(BaseModel):
    id: int
    category: str

    class Config:
        from_attributes = True


class RestaurantCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
    image_url: Optional[str] = None
    category_ids: List[int] = []


class RestaurantUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    category_ids: Optional[List[int]] = None


class RestaurantSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    location: str
    image_url: Optional[str] = None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantDetailSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    location: str
    image_url: Optional[str] = None
    owner_id: int
    created_at: datetime
    categories: List[CategorySchema] = []

    class Config:
        from_attributes = True
