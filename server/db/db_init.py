from datetime import datetime, timedelta

from app import Item, app, db

app.app_context().push()
db.drop_all()
item1 = Item(name='Тестовое имя 1', url='тест урл', description='тестовое описание для первого товара', price=1999,
             price_without_sale=2999, rating=4.5, delivery_time=datetime.now() + timedelta(days=4))
item2 = Item(name='Второе тестовое имя', url='тест урл', description='очень длинное описание для второго товара аваф оаофвлафлва вдфоа оаф д фвавфда вфа вфоа флоо ыфаф', price=1799,
             price_without_sale=2599, rating=4.86, delivery_time=datetime.now() + timedelta(days=1))
item3 = Item(name='Третье имя тест', url='тест урл', description='Короткое описание', price=2399,
             price_without_sale=3999, rating=4.44, delivery_time=datetime.now() + timedelta(days=2))
item4 = Item(name='Четвертое имя', url='тест урл', description='описание 4', price=2199,
             price_without_sale=3299, rating=4.7, delivery_time=datetime.now())
db.create_all()
db.session.add_all([item1, item2, item3, item4])
db.session.commit()
