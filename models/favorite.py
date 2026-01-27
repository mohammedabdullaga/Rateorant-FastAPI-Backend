from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel


class FavoriteModel(BaseModel):
    
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'restaurant_id', name='uq_user_restaurant_favorite'),)

    user = relationship('UserModel', back_populates='favorites')
    restaurant = relationship('RestaurantModel', back_populates='favorites')

    def __repr__(self):
        return f"<FavoriteModel(id={self.id}, user_id={self.user_id}, restaurant_id={self.restaurant_id})>"
