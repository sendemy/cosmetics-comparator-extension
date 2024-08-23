import requests
from fake_useragent import UserAgent as ua
from lxml import html

res = requests.get(
    'https://static-basket-01.wb.ru/vol0/data/'
    'main-menu-ru-ru-v2.json', headers={'Accept': "*/*",
                                        'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"})

print(res.content.decode())
