from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
from translate import Translator
import json

# перевод адресса с русского на английский и поиск координат с помощью Nominatim
# работает некорректно, найти другой способ
geolocator = Nominatim(user_agent="find_coordinate")

url = 'https://naturasiberica.ru/our-shops/'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

brand_name = soup.title.string[19:].strip()

shops = []
shop = {}

# получение всех ссылок на магазины и запись их в словарь
list_links = []
for link in soup.find_all('a'):
    try:
        if 'our-shops' in link.get('href'):
            link = 'https://naturasiberica.ru' + link.get('href')
            try:
                if str(link[37]):
                    list_links.append(link)
            except IndexError:
                pass
    except TypeError:
        pass


# получение всех адрессов и добвление их в словарь
# с последующим добавлением словаря в общий список
# добавление в словарь и в общий список имя бренда
try:
    # в ходе цикла переход во все ссылки списка list_links
    # из которого извлекаем график для каждого магазина
    # отсчет с двух, так как первые две ссылки не ведут в магазин
    idx_link = 2
    for address_city in soup.find_all(class_ = 'card-list__description'): # нахдим данные с адрессом магзина

        # приводим данные в удобный для обработки формат
        address_city = address_city.text
        address_city = address_city.replace('\r', '').replace('\t', '').strip()
        address_city_list = address_city.split('\n')
        address_ = address_city_list[1] + address_city_list[2]

        # помещаем данные в словарь shop
        shop['address'] = address_
        shop['name'] = brand_name

        # переходим по ссылке в магазин и переводим страницу в lxml
        link_html_text = requests.get(list_links[idx_link]).text
        link_soup = BeautifulSoup(link_html_text, 'lxml')

        # находим информацию о графике и приводим в удобный для обработки формат
        schedule = link_soup.find(class_ = 'original-shops__schedule').text.strip().replace('\r', '').replace('.', ':').replace('c ', '')
        schedule = schedule.split()

        # помещаем график в словарь shop
        # для всех магазинов один график
        # для всех магазинов один телефон
        # как извлечь график и телефон магазина из его id?
        shop['working_hours'] = ['пн-вс ' + schedule[1]]
        shop_copy = shop.copy()
        shops.append(shop_copy) # помещаем словаь в список shops
        shop.clear()
        idx_link += 1
        print(shops)
except (TypeError, IndexError, RuntimeError):
    pass

json_shops = json.dumps(shops)
print(json_shops)
