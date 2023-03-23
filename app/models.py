from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text


class Post(Base):
    __tablename__ = "posts"         # This is the name of the table in the database
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('NOW()'))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, server_default='TRUE', default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('NOW()'))
