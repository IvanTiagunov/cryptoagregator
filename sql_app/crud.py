from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_news_by_title(db: Session, title: str):
    return db.query(models.News).filter(models.News.title == title).order_by(models.News.date_of_append.desc()).first()


def get_news_by_id(db: Session, news_id: int):
    result = db.query(models.News).filter(models.News.id == news_id).first()
    return result


def delete_news_by_id(db: Session, news: Session.query):
    db.delete(news)
    db.commit()
    return news


def get_all_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.News).offset(skip).limit(limit).all()


def create_news(db: Session, news: schemas.NewsCreate):
    dt = datetime.now()
    db_news = models.News(
        resource=news.resource,
        title=news.title,
        date=news.date,
        link=news.link,
        date_of_append=dt
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def update_news(db, db_news, new_news):
    news_data = new_news.dict(exclude_unset=True)
    for key, value in news_data.items():
        if key == 'date_of_append':
            value = datetime.now()
        setattr(db_news, key, value)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news
