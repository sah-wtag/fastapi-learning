from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    email: str


class CreateUser(User):
    email: EmailStr
    password: str


class UserResponse(User):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
