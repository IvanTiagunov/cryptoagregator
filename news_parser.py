import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Integer, String, Column, DateTime
from sqlalchemy.orm import Session

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

# TODO можно сделать общий парсер, а затем подставлять в него значения


Base = declarative_base()


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    resource = Column(String)
    title = Column(String)
    date = Column(String)
    link = Column(String)
    date_of_append = Column(DateTime)


# БД
# TODO сделать базу данных по примеру из второго пайчарма


engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

# парсер для bits.media
def parse_bitsmedia():
    page = requests.get('https://bits.media/').content
    soup = BeautifulSoup(page, features='html.parser')
    items = soup.find_all('div', class_='news-content')

    for item in items:
        session = Session(bind=engine)
        resource = 'https://bits.media/'
        title = item.find('h2', class_='news-name').get_text()
        date = item.find('span', class_='news-date').get_text()
        link = item.find('a', class_='news-link')['href']
        dt = datetime.now()

        session.add(
            News(
                resource=resource,
                title=title,
                date=date,
                link=link,
                date_of_append=dt
            )
        )
        session.commit()

    # db.write(news)


#парсер риа новости
def parse_ria():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
    }
    page = requests.get('https://ria.ru/product_kriptovalyuta/', headers=headers).content
    soup = BeautifulSoup(page, features='html.parser')
    items = soup.find_all('div', class_='list-item')
    # print(items)
    for item in items:
        session = Session(bind=engine)
        resource = 'https://ria.ru/product_kriptovalyuta/'
        title = item.find('a', class_='list-item__title color-font-hover-only').get_text()
        date = item.find('div', class_='list-item__date').get_text()
        link = item.find('a', class_='list-item__title color-font-hover-only')['href']
        dt = datetime.now()
        # print(resource, title, date, link, dt)
        session.add(
            News(
                resource=resource,
                title=title,
                date=date,
                link=link,
                date_of_append=dt
            )
        )
        session.commit()


def parse_rbk():
    #
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
    }
    page = requests.get('https://www.rbc.ru/crypto/', headers=headers).content
    soup = BeautifulSoup(page, features='html.parser')
    items = soup.find_all('div', class_='item')
    for item in items:
        session = Session(bind=engine)
        resource = 'https://www.rbc.ru/crypto/'
        try :
            title = item.find('span', class_='item__title rm-cm-item-text').get_text().strip()
        except:
            title = 'Not found'
            continue
        item_link= item.find('a', class_='item__link')['href']
        item_page = requests.get(item_link, headers=headers).content
        item_soup = BeautifulSoup(item_page, features='html.parser')
        date = item_soup.find('time', class_='article__header__date')['datetime']
        link = item_link
        dt = datetime.now()

        session.add(
            News(
                resource=resource,
                title=title,
                date=date,
                link=link,
                date_of_append=dt
            )
        )
        session.commit()
if __name__ == '__main__':
    #parse_bitsmedia()
    # parse_ria()
    # parse_rbk()
    print('status ok')
