from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel


class ReviewModel(BaseModel):
    
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'restaurant_id', name='uq_user_restaurant_review'),)

    user = relationship('UserModel', back_populates='reviews')
    restaurant = relationship('RestaurantModel', back_populates='reviews')

    def __repr__(self):
        return f"<ReviewModel(id={self.id}, user_id={self.user_id}, restaurant_id={self.restaurant_id}, rating={self.rating})>"
