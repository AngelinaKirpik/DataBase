import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models_additionaltask2 import create_tables, Publisher, Book, Stock, Shop, Sale
from settings import postgres_login, postgres_password

DSN = f'postgresql://{postgres_login}:{postgres_password}@localhost:5432/books_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json.txt', encoding='utf-8') as f:
    data = json.load(f)
    model_map = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }

    for item in data:
        model_name = item['model']
        pk = item['pk']
        fields = item['fields']
        model_class = model_map[model_name]

        existing = session.query(model_class).filter(model_class.id == pk).first()
        if existing:
            continue

        obj = model_class(id=pk, **fields)
        session.add(obj)
    session.commit()
    print('Данные успешно загружены')
user_input = input("Введите имя или id издателя: ")

if user_input.isdigit():
    condition = Publisher.id == int(user_input)
else:
    condition = Publisher.name == user_input

results = session.query(
    Book.title,
    Shop.name,
    Sale.price,
    Sale.date_sale
    ).join(Stock, Sale.id_stock == Stock.id) \
           .join(Book, Stock.id_book == Book.id) \
           .join(Publisher, Book.id_publisher == Publisher.id) \
           .join(Shop, Stock.id_shop == Shop.id) \
           .filter(condition) \
           .all()

if results:
    print(f"Название книги | Название магазина | Стоимость | Дата продажи ")
    for title, shop_name, price, date_sale in results:
        date_str = date_sale.strftime('%d-%m-%y') if date_sale else ''

        print(f"{title} | {shop_name} | {price} | {date_str}")
else:
    print("Продажи книг этого издателя не найдены")

session.close()