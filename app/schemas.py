from datetime import datetime
from pydantic import BaseModel, EmailStr


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

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
