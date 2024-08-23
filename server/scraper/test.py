import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua


def save(comp):
    with open('price_info.txt', 'a') as file:
        file.write(f"{comp['title']}->price:{comp['price']}->{comp['link']}\n")


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


url = 'https://www.wildberries.ru/catalog/16518622/detail.aspx'

parse(url)
