import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from sql_app.crud import *
from sql_app.database import Base

eng_sites = [
    'https://economictimes.indiatimes.com/',
    'https://www.coindesk.com/',
    'https://news.bitcoin.com/',
]

ru_sites = [
    'https://bits.media/',
    'https://ria.ru/product_kriptovalyuta/'
    'https://www.rbc.ru/crypto/',
    'https://ru.investing.com/news/cryptocurrency-news',
    'https://iz.ru/tag/kriptovaliuta',
    'https://1prime.ru/trend/bitcoins/'
]


# подключение к БД
SQLALCHEMY_DATABASE_URL="sqlite:///sql_app/database.sqlite"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
}


def parse_base(site_url: str, items_tag: str, items_class: str):
    page = requests.get(url=site_url, headers=headers).content
    soup = BeautifulSoup(page, features='html.parser')
    items = soup.find_all(items_tag, class_=items_class)
    return items


def check_item(title: str, db: Session):
    return get_news_by_title(db=db, title=title)


def append_item_to_db(resource, title, date, link, dt):
    db = Session(bind=engine)
    db_news = check_item(title=title, db=db)

    if db_news:
        # можно помечать в отдельную базу данных, что посты повторяются, чтобы изменить задержку парсинга для  сайта
        # в идеале конечно получать новости по триггеру - изменение страницы...
        print(f'{db_news} was skipped because it is already in DB')
        print(db_news)

    else:
        db_news = models.News(
            resource=resource,
            title=title,
            date=date,
            link=link,
            date_of_append=dt
        )

        db.add(db_news)
        db.commit()
        db.refresh(db_news)
    db.close()


# парсер для bits.media
def parse_bitsmedia():
    url = 'https://bits.media/'
    items = parse_base(site_url=url, items_tag='div', items_class='news-content')

    for item in items:
        resource = url
        title = item.find('h2', class_='news-name').get_text()
        date = item.find('span', class_='news-date').get_text()
        link = item.find('a', class_='news-link')['href']
        dt = datetime.now()
        append_item_to_db(resource, title, date, link, dt)


# парсер риа новости
def parse_ria():
    url = 'https://ria.ru/product_kriptovalyuta/'
    items = parse_base(site_url=url, items_tag='div', items_class='list-item')
    for item in items:
        resource = url
        title = item.find('a', class_='list-item__title color-font-hover-only').get_text()
        date = item.find('div', class_='list-item__date').get_text()
        link = item.find('a', class_='list-item__title color-font-hover-only')['href']
        dt = datetime.now()
        append_item_to_db(resource, title, date, link, dt)


def parse_rbk():
    url = 'https://www.rbc.ru/crypto/'
    items = parse_base(site_url=url, items_tag='div', items_class='item')
    for item in items:
        resource = url
        try:
            title = item.find('span', class_='item__title rm-cm-item-text').get_text().strip()
        except:
            title = 'Not found'
            continue
        link = item.find('a', class_='item__link')['href']
        item_page = requests.get(link, headers=headers).content
        item_soup = BeautifulSoup(item_page, features='html.parser')
        date = item_soup.find('time', class_='article__header__date')['datetime']
        dt = datetime.now()

        append_item_to_db(resource, title, date, link, dt)


def parse_investcom():
    url = 'https://ru.investing.com/news/cryptocurrency-news'
    items = parse_base(site_url=url, items_tag='div', items_class='textDiv')
    for item in items:

        resource = url
        try:
            title = item.find('a', class_='title')['title']
            if len(title) == 0:
                continue
        except:
            continue  # print('something wrong with title')
        try:
            link = item.find('a', class_='title')['href']
        except:
            continue  # print('something wrong with link')
        try:
            date = item.find('span', class_='date').get_text()
        except:
            continue
        dt = datetime.now()



        append_item_to_db(resource, title, date, link, dt)
        # print(resource, title, date, link, dt)


if __name__ == '__main__':
    # parse_bitsmedia()
    # parse_ria()
    parse_rbk()
    # print('status ok')
    # parse_investcom()
