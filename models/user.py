from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime, func
from .base import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import relationship
from config.environment import secret
import enum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"
    restaurant_owner = "restaurant_owner"

class UserModel(BaseModel):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.user, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    reviews = relationship('ReviewModel', back_populates='user', cascade="all, delete-orphan")
    favorites = relationship('FavoriteModel', back_populates='user', cascade="all, delete-orphan")
    owned_restaurants = relationship('RestaurantModel', back_populates='owner', cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(self.id),
            "username": self.username,
            "role": self.role.value,  # Convert enum to string value
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return token
