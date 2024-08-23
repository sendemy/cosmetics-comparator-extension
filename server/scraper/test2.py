import datetime
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua


def get_catalogs_wb(url: str, headers: dict):
    return requests.get(url, headers=headers).json()


def get_data_category(catalogs_wb: dict) -> list:
    catalog_data = []
    if isinstance(catalogs_wb, dict) and 'childs' not in catalogs_wb:
        catalog_data.append({
            'name': f"{catalogs_wb['name']}",
            'shard': catalogs_wb.get('shard', None),
            'url': catalogs_wb['url'],
            'query': catalogs_wb.get('query', None)
        })
    elif isinstance(catalogs_wb, dict):
        catalog_data.extend(get_data_category(catalogs_wb['childs']))
    else:
        for child in catalogs_wb:
            catalog_data.extend(get_data_category(child))
    return catalog_data


def search_category_in_catalog(url: str, catalog_list: list) -> dict:
    """проверка пользовательской ссылки на наличии в каталоге"""
    for catalog in catalog_list:
        if catalog['url'] == url.split(url)[-1]:
            print(f'найдено совпадение: {catalog["name"]}')
            return catalog


def get_data_from_json(json_file: dict) -> list:
    """извлекаем из json данные"""

    data_list = []
    for data in json_file['data']['products']:
        sku = data.get('id')
        name = data.get('name')
        price = int(data.get("priceU") / 100)
        salePriceU = int(data.get('salePriceU') / 100)
        cashback = data.get('feedbackPoints')
        sale = data.get('sale')
        brand = data.get('brand')
        rating = data.get('rating')
        supplier = data.get('supplier')
        supplierRating = data.get('supplierRating')
        feedbacks = data.get('feedbacks')
        reviewRating = data.get('reviewRating')
        promoTextCard = data.get('promoTextCard')
        promoTextCat = data.get('promoTextCat')
        data_list.append({
            'id': sku,
            'name': name,
            'price': price,
            'salePriceU': salePriceU,
            'cashback': cashback,
            'sale': sale,
            'brand': brand,
            'rating': rating,
            'supplier': supplier,
            'supplierRating': supplierRating,
            'feedbacks': feedbacks,
            'reviewRating': reviewRating,
            'promoTextCard': promoTextCard,
            'promoTextCat': promoTextCat,
            'link': f'https://www.wildberries.ru/catalog/{data.get("id")}/detail.aspx?targetUrl=BP'
        })
    return data_list


def scrap_page(page: int, shard: str, query: str, low_price: int, top_price: int, discount: int = None) -> dict:
    """Сбор данных со страниц"""
    headers = {{"user_agent": ua().random}}
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub' \
        f'&dest=-1257786' \
        f'&locale=ru' \
        f'&page={page}' \
        f'&priceU={low_price * 100};{top_price * 100}' \
        f'&sort=popular&spp=0' \
        f'&{query}' \
        f'&discount={discount}'
    r = requests.get(url, headers=headers)
    print(f'Статус: {r.status_code} Страница {page} Идет сбор...')
    return r.json()


def save(data: list, filename: str):
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(f'{filename}.txt')
    df.to_excel(writer, sheet_name='data', index=False)
    writer.sheets['data'].set_column(0, 1, width=10)
    writer.sheets['data'].set_column(1, 2, width=34)
    writer.sheets['data'].set_column(2, 3, width=8)
    writer.sheets['data'].set_column(3, 4, width=9)
    writer.sheets['data'].set_column(4, 5, width=8)
    writer.sheets['data'].set_column(5, 6, width=4)
    writer.sheets['data'].set_column(6, 7, width=20)
    writer.sheets['data'].set_column(7, 8, width=6)
    writer.sheets['data'].set_column(8, 9, width=23)
    writer.sheets['data'].set_column(9, 10, width=13)
    writer.sheets['data'].set_column(10, 11, width=11)
    writer.sheets['data'].set_column(11, 12, width=12)
    writer.sheets['data'].set_column(12, 13, width=15)
    writer.sheets['data'].set_column(13, 14, width=15)
    writer.sheets['data'].set_column(14, 15, width=67)
    writer.close()
    print(f'Все сохранено в {filename}.txt\n')


def parse(url):
    headers = {"user_agent": ua().random}
    response = requests.get(url, headers=headers)
    print(response.content)
    soup = BeautifulSoup(response.content, features="lxml")
    items = soup.find_all('div', className='price-block__wallet-price')
    comps = []

    for item in items:
        comps.append({
            'title': item.find("a", class_="product-page__title").get_text(strip=True),
            "price": item.find("p", class_="price-block__wallet-price").get_text(strip=True),
            'link': item.find("h1", class_="product-page__title").get_text(strip=True),
        })
        print(f"{item['title']}->price:{item['price']}->{item['link']}")
        save(item)


def parser(url: str, low_price: int = 1, top_price: int = 1000000, discount: int = 0):
    """основная функция"""
    # получаем данные по заданному каталогу
    catalog_data = get_data_category(get_catalogs_wb(url, None))
    try:
        category = search_category_in_catalog(
            url=url, catalog_list=catalog_data)
        data_list = []
        for page in range(1, 101):
            data = scrap_page(
                page=page,
                shard=category['shard'],
                query=category['query'],
                low_price=low_price,
                top_price=top_price,
                discount=discount)
            print(f'Добавлено позиций: {len(get_data_from_json(data))}')
            if len(get_data_from_json(data)) > 0:
                data_list.extend(get_data_from_json(data))
            else:
                break
        print(f'Сбор данных завершен. Собрано: {len(data_list)} товаров.')
        # сохранение найденных данных
        save(data_list, f'{category["name"]}_from_{low_price}_to_{top_price}')
        print(f'Ссылка для проверки: {url}?priceU={
              low_price * 100};{top_price * 100}&discount={discount}')
    except TypeError:
        print('Ошибка! Возможно не верно указан раздел. Удалите все доп фильтры с ссылки')
    except PermissionError:
        print('Ошибка! Вы забыли закрыть созданный ранее excel файл. Закройте и повторите попытку')


headers = {"user_agent": ua().random}
url = 'https://www.wildberries.ru/catalog/219503618/detail.aspx'

parser(url)
