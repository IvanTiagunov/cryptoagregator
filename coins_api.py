'''
Возвращает цены монет из моего апи
'''

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Coin(BaseModel):
    name: str
    price: float

Coins_list = [
    Coin(name='bitcoin',price=2000),
    Coin(name='litecoin', price=50),
    Coin(name='etherium', price=280)
]

@app.get("/coins")
def read_coins_list():
    return Coins_list

@app.put("/coin/create")
def create_coin(coin: Coin):
    Coins_list.append(coin)
    return {"status":"ok"}


@app.get("/coin/{coin_id}")
def read_coin(coin_id: int):
    coin = Coins_list[coin_id]
    return {"coin_name":coin.name, "coin_price": coin.price}


@app.put("/coin/{coin_id}")
def update_coin(coin_id: int, coin: Coin):
    return {"status":"ok"}


@app.delete("/coin/{coin_id}")
def delete_coin(coin_id: int):

    if coin_id < 0 or len(Coins_list) < 0 or len(Coins_list) - 1 < coin_id  :
        message = "can't remove coin, because it's not in list"
    else:
        coin = Coins_list[coin_id]
        Coins_list.remove(coin)
        message = f"coin {coin.name} was deleted"
    return {"status": message}

