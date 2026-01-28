from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from models.restaurant import RestaurantModel
from models.notification import NotificationModel
from models.user import UserModel

from serializers.notification import NotificationSchema

from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter(tags=["notifications"]) 

@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict])
def get_notifications(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get notifications for restaurants owned by the current user"""
    owner_restaurants = db.query(RestaurantModel).filter(RestaurantModel.owner_id == current_user.id).all()
    if not owner_restaurants:
        return []
    restaurant_ids = [r.id for r in owner_restaurants]

    notifications = (
        db.query(NotificationModel)
        .filter(NotificationModel.restaurant_id.in_(restaurant_ids))
        .order_by(NotificationModel.created_at.desc())
        .all()
    )

    result = []
    for n in notifications:
        restaurant = next((r for r in owner_restaurants if r.id == n.restaurant_id), None)
        user = db.query(UserModel).filter(UserModel.id == n.user_id).first()
        result.append({
            "id": n.id,
            "restaurant_id": n.restaurant_id,
            "restaurant_name": restaurant.name if restaurant else "",
            "user_name": user.username if user else "",
            "rating": n.rating,
            "message": n.message,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "read": n.read,
        })

    return result
