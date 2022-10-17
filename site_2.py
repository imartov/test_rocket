from bs4 import BeautifulSoup
import requests

# получаем url страницы
url = 'https://som1.ru/shops/'
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)
html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')

# находим id всех магазинов и помещаем их в список
# как перейти в каждый магазин по его id и извлечь нужную информацию?
id_shops_list = []
for input_ in soup.find_all('input'):
    id_shop = input_.get('id')
    try:
        if id_shop.isdigit():
            id_shops_list.append(id_shop)
    except AttributeError:
        pass

print(id_shops_list)

