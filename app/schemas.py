from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Authentication Schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user: "User"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithPosts(User):
    posts: List["Post"] = []

    class Config:
        from_attributes = True


# Post Schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: int = 0


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[int] = None


class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostWithAuthor(Post):
    author: User

    class Config:
        from_attributes = True
