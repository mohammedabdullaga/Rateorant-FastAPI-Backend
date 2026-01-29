from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import BaseModel


class NotificationModel(BaseModel):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    rating = Column(Integer, nullable=True)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    restaurant = relationship('RestaurantModel', back_populates='notifications')
    user = relationship('UserModel')

    def __repr__(self):
        return f"<Notification(id={self.id}, restaurant_id={self.restaurant_id}, user_id={self.user_id})>"
