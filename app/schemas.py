from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class User(BaseModel):
    email: str


class CreatePost(PostBase):
    pass


class UserResponse(User):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PostResponse(PostBase):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserResponse

    model_config = {"from_attributes": True}


class CreateUser(User):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
