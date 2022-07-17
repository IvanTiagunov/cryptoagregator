from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    resource = Column(String)
    title = Column(String)
    date = Column(String)
    link = Column(String)
    date_of_append = Column(DateTime)

    def __repr__(self):
        return f'{self.title}'
