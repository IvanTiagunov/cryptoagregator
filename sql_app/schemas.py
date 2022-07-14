from pydantic import BaseModel
from datetime import datetime
from typing import Optional
'''
Pydantic models
'''


class NewsBase(BaseModel):
    resource: str
    title: str
    date: str
    link: str
    date_of_append: datetime


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int

    class Config:
        orm_mode = True


class NewsUpdate(BaseModel):
    resource: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    date_of_append: datetime