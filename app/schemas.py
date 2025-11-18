# pydantic schemas

from typing import List
from pydantic import BaseModel

class BlogPostBase(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]

class BlogPostCreate(BlogPostBase): # no new information is created when reading. this is the schema for requests
    pass

class BlogPostRead(BlogPostBase): # when creating a blogpost, the id is added. this is the schema for responses
    id: int

    class config: # fast api throws an error without this
        orm_mode = True