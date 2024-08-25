import datetime
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua
from retry import retry

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.wildberries.ru",
    'Content-Type': 'application/json; charset=utf-8',
    'Transfer-Encoding': 'chunked',
    "Connection": "keep-alive",
    'Vary': 'Accept-Encoding',
    'Content-Encoding': 'gzip',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site"
}
catalag_url = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'


def get_catalogs_wb() -> dict:
    "полный католог товаров WB"
    return requests.get(catalog_url, haeders=HEADERS).json()


def get_data_category(catalogs_wb: dict) -> list:
    "сбор данных категорий из WB"
    catalog_data = []
    if isinstance(catalogs_wb, dict) and 'childs' not in catalogs_wb:
        catalog_data.append({
            'name': f"{catalogs_wb['name']}",
            'shard': catalogs_wb.get('shard', None),
            'url': catalogs_wb['url'],
            'querly': catalogs_wb.get('querly', None),
        })
    elif isinstance(catalogs_wb, dict):
        catalog_data.extend(get_data_category(catalogs_wb['childs']))
    else:
        for child in catalogs_wb:
            catalogs_data.extend(get_data_category(child))
    return catalog_data


def search_category_in_catalog(url: str, catalog_list: list) -> dict:
    'пров польз ссылки на налич в каталоге'
    for catalog in catalog_list:
        if catalog['url'] == url.split('https://www.wildberries.ru')[-1]:
            print(f'найдено совпадение: {catalog["name"]}')
            return catalog


def get_data_from_json(json_file: dict) -> list:
    data_list = []
    for data in json_file['data']['products']:
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
            'link': f'https://www.wildberries.ru/catalog/{data.get("id")}/detail.aspx'
        })
    return data_list


@retry(Exception, tries=-1, delay=0)
def scrap_page(page: int, shard: str, query: str, low_price: int, top_price: int, discount: int = None) -> dict:
    'сбор данных со страниц'
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub' \
        f'&dest=-1257786' \
        f'&locale=ru' \
        f'&page={page}' \
        f'&priceU={low_price * 100};{top_price * 100}' \
        f'&sort=popular&spp=0' \
        f'&{query}' \
        f'&discount={discount}'

    r = requests.get(url, headers=headers)
    print(f'Статус: {r.status_code} Страница {page}')
    return r.json()


def save_excel(data: list, filename: str):
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(f'{filename}.xlsx')
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
    print(f'Все сохранено в {filename}.xlsx\n')


def parser(url: str, low_price: int = 1, top_price: int = 1000000, discount: int = 0):
    'оснавн функция'
    catalog_data = get_data_category(get_catalogs_wb())
    try:
        category = search_category_in_catalog(
            url=url, catalog_list=catalog_data)
        data_list = []
        for page in range(1, 51):
            data = scrap_page(
                page=page,
                shard=category['shard'],
                query=category['query'],
                low_price=low_price,
                top_price=top_price,
                discount=discount)
            if len(get_data_from_json(data)) > 0:
                data_list.extend(get_data_from_json(data))
            else:
                break
            print(f'Сбор данных завершен. Собрано: {len(data_list)} товаров.')
            # сохранение найденных данных
            save_excel(data_list, f'{category["name"]}_from_{
                       low_price}_to_{top_price}')
            print(f'Ссылка для проверки: {url}?priceU={
                  low_price * 100};{top_price * 100}&discount={discount}')
    except TypeError:
        print(
            'Ошибка! Возможно не верно указан раздел. Удалите все доп фильтры с ссылки')
        # except PermissionError:
        #    print('Ошибка! Вы забыли закрыть созданный ранее excel файл. Закройте и повторите попытку')


if __name__ == '__main__':
    url = input('Введите ссылку на категорию без фильтров для сбора:\n')
    low_price = 0
    top_price = 10**10
    discond = 0
    start_datetime.datetim.now()

    parser(url=url, low_price=low_price,
           top_price=top_price, discount=discount)

    end = datetime.datetime.now()
    total = end-start
    print('время работы:'+str(total))
