from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, conint


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserComment(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Comment(BaseModel):
    post_id: int
    content: str

    class Config:
        orm_mode = True


class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    owner: Optional[UserComment] = Field(
        None, description="The user who wrote the comment")

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    # Because there is PostBase in argument, it will inherit all the attributes from PostBase
    pass
    # pass is a null statement in python it tells python that class is empty


class Post(PostBase):
    # No need to title, content, published because they are inherited from PostBase
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # le = less than or equal to
