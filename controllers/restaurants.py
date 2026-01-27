from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models.restaurant import RestaurantModel
from models.review import ReviewModel
from models.favorite import FavoriteModel
from models.category import CategoryModel
from models.user import UserModel, RoleEnum
# Serializers
from serializers.restaurant import RestaurantSchema, RestaurantCreateSchema, RestaurantUpdateSchema, RestaurantDetailSchema, CategorySchema
from serializers.review import ReviewSchema, ReviewCreateSchema
from serializers.favorite import FavoriteSchema
from typing import List
# Database Connection
from database import get_db
# Middleware
from dependencies.get_current_user import get_current_user

security = HTTPBearer()

router = APIRouter()

@router.get("/restaurants", response_model=List[RestaurantSchema])
def get_restaurants(db: Session = Depends(get_db)):
    """Get all restaurants"""
    restaurants = db.query(RestaurantModel).all()
    return restaurants


@router.get("/categories", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    """Get all available categories"""
    categories = db.query(CategoryModel).all()
    return categories


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantDetailSchema)
def get_single_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Get a single restaurant with details"""
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return restaurant


@router.post('/restaurants', response_model=RestaurantSchema)
def create_restaurant(
    restaurant: RestaurantCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new restaurant - only restaurant_owner or admin"""
    if current_user.role not in [RoleEnum.restaurant_owner, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Only restaurant owners or admins can create restaurants")

    restaurant_data = restaurant.dict(exclude={'category_ids'})
    new_restaurant = RestaurantModel(**restaurant_data, owner_id=current_user.id)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    if restaurant.category_ids:
        categories = db.query(CategoryModel).filter(CategoryModel.id.in_(restaurant.category_ids)).all()
        new_restaurant.categories.extend(categories)
        db.commit()

    return new_restaurant


@router.put('/restaurants/{restaurant_id}', response_model=RestaurantSchema)
def update_restaurant(
    restaurant_id: int,
    restaurant: RestaurantUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a restaurant - owner or admin only"""
    db_restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()

    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if db_restaurant.owner_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Permission Denied")


    update_data = restaurant.dict(exclude_unset=True, exclude={'category_ids'})
    for field, value in update_data.items():
        if value is not None:
            setattr(db_restaurant, field, value)

    if restaurant.category_ids is not None:
        categories = db.query(CategoryModel).filter(CategoryModel.id.in_(restaurant.category_ids)).all()
        db_restaurant.categories = categories

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


@router.delete('/restaurants/{restaurant_id}')
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a restaurant - owner or admin only"""
    db_restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()

    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if db_restaurant.owner_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Permission Denied")

    db.delete(db_restaurant)
    db.commit()

    return {"message": "Restaurant deleted successfully"}



@router.get("/restaurants/{restaurant_id}/reviews", response_model=List[ReviewSchema])
def get_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific restaurant"""
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    reviews = db.query(ReviewModel).filter(ReviewModel.restaurant_id == restaurant_id).all()
    return reviews


@router.post('/restaurants/{restaurant_id}/reviews', response_model=ReviewSchema)
def create_review(
    restaurant_id: int,
    review: ReviewCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a review for a restaurant"""
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    existing_review = db.query(ReviewModel).filter(
        ReviewModel.user_id == current_user.id,
        ReviewModel.restaurant_id == restaurant_id
    ).first()

    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this restaurant")

    new_review = ReviewModel(
        **review.dict(),
        user_id=current_user.id,
        restaurant_id=restaurant_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.get("/restaurants/{restaurant_id}/favorite")
def check_favorite(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Check if restaurant is marked as favorite"""
    favorite = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == current_user.id,
        FavoriteModel.restaurant_id == restaurant_id
    ).first()

    return {"is_favorite": favorite is not None}


@router.post('/restaurants/{restaurant_id}/favorite', response_model=FavoriteSchema)
def add_favorite(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Add restaurant to favorites"""
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    existing_favorite = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == current_user.id,
        FavoriteModel.restaurant_id == restaurant_id
    ).first()

    if existing_favorite:
        raise HTTPException(status_code=400, detail="Restaurant already in favorites")

    new_favorite = FavoriteModel(user_id=current_user.id, restaurant_id=restaurant_id)
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    return new_favorite


@router.delete('/restaurants/{restaurant_id}/favorite')
def remove_favorite(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Remove restaurant from favorites"""
    favorite = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == current_user.id,
        FavoriteModel.restaurant_id == restaurant_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()

    return {"message": "Restaurant removed from favorites"}


@router.get("/favorites", response_model=List[FavoriteSchema])
def get_my_favorites(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all favorite restaurants for current user"""
    favorites = db.query(FavoriteModel).filter(FavoriteModel.user_id == current_user.id).all()
    return favorites
