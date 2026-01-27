from pydantic import BaseModel
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
