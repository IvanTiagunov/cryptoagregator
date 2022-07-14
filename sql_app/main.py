from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
from crud import *
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/news/", response_model=schemas.News)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_title(db, title=news.title)
    if db_news:
        raise HTTPException(status_code=400, detail="News already exists")
    return crud.create_news(db=db, news=news)


@app.get("/news/", response_model=list[schemas.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_news(db, skip=skip, limit=limit)


@app.get("/news/{news_id}", response_model=schemas.News)
def read_news_by_id(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_id(db, news_id=news_id)
    if not db_news:
        raise HTTPException(status_code=400, detail="Such id doesn't exist")
    return db_news


@app.patch("/news/{news_id}", response_model=schemas.News)
def update_news_by_id(news_id: int, new_news: schemas.NewsUpdate, db: Session = Depends(get_db)):
    #checks if news already exists
    old_news = read_news_by_id(news_id=news_id, db=db)
    return crud.update_news(db, db_news = old_news, new_news =new_news )


@app.delete("/news/{news_id}", response_model=schemas.News)
def delete_news_by_id(news_id: int, db: Session = Depends(get_db)):
    # checks if news already exists
    checked_news = read_news_by_id(news_id=news_id, db=db)
    return crud.delete_news_by_id(db, news = checked_news)



