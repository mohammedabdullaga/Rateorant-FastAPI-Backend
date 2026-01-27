from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import BaseModel


class RestaurantModel(BaseModel):
    
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=False, index=True)
    image_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    owner = relationship('UserModel', back_populates='owned_restaurants')
    reviews = relationship('ReviewModel', back_populates='restaurant', cascade="all, delete-orphan")
    favorites = relationship('FavoriteModel', back_populates='restaurant', cascade="all, delete-orphan")
    categories = relationship('CategoryModel', secondary='restaurant_categories', back_populates='restaurants')

    def __repr__(self):
        return f"<RestaurantModel(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
