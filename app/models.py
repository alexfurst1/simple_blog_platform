# what sqlalchemy (our ORM) needs to be able to create the tables we need in the mysql database
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, Text
from .database import Base
from sqlalchemy.dialects.mysql import JSON

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(Integer, primary_key=True,index=True)

    title = Column(String(255),nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    tags = Column(JSON, nullable=False)

    # defines the table sqlalchemy will create

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())