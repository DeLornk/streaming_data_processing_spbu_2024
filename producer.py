import faust
import random
import time

from faker import Faker
import datetime as datetime
import pandas as pd
import random as rand


df_apple = pd.DataFrame(columns=['market','country', 'product','color','price','card', 'id', 'time'])

list_market = ['OZON', 'Wildberries','Яндекс Маркет', 're:Store','Мегамаркет','М.Видео',
              'Эльдорадо', 'Ситилинк','DNS', 'Технопарк','Связной','Билайн','Мегафон','t2']

list_prod = ['iPhone 16','iPhone 16 Plus','iPhone 16 Pro','iPhone 16 Pro Max', 
             'Apple Watch 10','Apple Watch Ultra 2','AirPods 4','AirPods Max', 
             'iPad','iPad Pro','iPad Air','iPad mini', 'Vision Pro','MacBook Air', 'MacBook Pro']

list_color = ['midnight','starlight','blue','purple','space black','silver','green','yellow','pink',
              'black', 'white', 'plata', 'gold', 'negro', 'rosa', 'amarillo', 'red', 'azul', 'grafito','verde']

class Order(faust.Record, serializer='json'):
    market: str
    country: str
    product: str
    color: str
    price: float
    time: str

app = faust.App('my_app', broker='127.0.0.1:9092')

topic = app.topic('my_topic', value_serializer='json')

fake = Faker('ru_RU')

@app.timer(interval=1.0)
async def generate_number():
    message = Order(
        market=random.choice(list_market),
        country=fake.city_name(),
        product=random.choice(list_prod),
        color=random.choice(list_color),
        price=round(random.uniform(90, 300), 1),
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # время появления объявления (не появления в нашей системе)
    )

    await topic.send(value=message)
    print(f"Sent message: {message}")

if __name__ == '__main__':
    app.main()
