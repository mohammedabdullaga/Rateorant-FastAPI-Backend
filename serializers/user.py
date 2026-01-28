from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserRegistrationSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserTokenSchema(BaseModel):
    token: str
    message: str


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetailSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True