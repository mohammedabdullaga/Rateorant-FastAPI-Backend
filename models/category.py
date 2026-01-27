from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


restaurant_categories = Table(
    'restaurant_categories',
    BaseModel.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)


class CategoryModel(BaseModel):
    
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, unique=True, index=True)

    restaurants = relationship('RestaurantModel', secondary=restaurant_categories, back_populates='categories')

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name})>"
