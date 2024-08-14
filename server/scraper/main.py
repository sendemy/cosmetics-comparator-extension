import requests
from lxml import html

websites = [
    'https://www.wildberries.ru/'
]

res = requests.get(
    'https://www.wildberries.ru/catalog/21646648/detail.aspx')
print(res.content[:20])
# content = res.content.decode("utf-8")
# tree = html.fromstring(content)
# element = tree.xpath(
#     '/html/body/div[1]')
# print(element)
# print(content)
