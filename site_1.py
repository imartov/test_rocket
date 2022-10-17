from bs4 import BeautifulSoup
import requests
import json
from geopy.geocoders import Nominatim

# получаем url сайта
url = 'https://oriencoop.cl/sucursales.htm'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

# получаем имя бренда
oriencoop_name = soup.title.string[11:]

# получаем общие телефоны и помещаем их в список phones_
phones_ = []
phones = soup.find('div', class_ = 'b-call shadow').text
phones = phones.split('\n')
for value in phones:
    try:
        if value[1].isdigit():
            phones_.append(value)
    except IndexError:
        pass

# получаем ссылки на все города и помещаем их в список list_links
list_links = []
for link in soup.find_all('a'):
    try:
        if 'sucursales' in link.get('href'):
            link = 'https://oriencoop.cl/' + link.get('href')
            list_links.append(link)
    except TypeError:
        pass

# создаем внешний список, в который будем помещать словарь с данными
cities = []

# создаем словарь, в который будем помещать данные о каждом городе
city = {}

# подтягиваем геолокатор для поиска координат
geolocator = Nominatim(user_agent="find_coordinate")

# создаем цикл, на каждой итерации которого переходим по ссылке
# в словаре list_links и извлекаем нужные данные
try:
    for idx_city, link in enumerate(list_links[1:-1]):
        html_text_link = requests.get(link).text # получаем url каждой страницы из списка
        soup_link = BeautifulSoup(html_text_link, 'lxml')
        direction = soup_link.find('div', 's-dato').text # находим в url класс с нужной информацией и помещаем в словарь city
        direction = direction.split('\n') # преобразовываем найденные данные в список для удобства обработки
        for idx, value in enumerate(direction):
            if value == 'Dirección:':
                city['address'] = direction[idx + 1].replace('í', 'i') # получаем адресс и помешаем в словарь
                location = geolocator.geocode(city['address']) # получаем координаты по адресу
                city['latlon'] = [location.latitude, location.longitude] # заносим координаты в словарь
                city['name'] = oriencoop_name # помещаем имя бренда в словарь
            elif value == 'Teléfono:':
                city['phones'] = [direction[idx + 1]] + phones_ # помещаем телефоны в словарь
            elif value == 'Horarios:':
                list_hours_1 = direction[idx + 1].split() # получаем время работы
                list_hours_2 = direction[idx + 2].split()
                hours = []
                # помещаем время работы (только часи и минуты, без текста) в список hours
                for hour in list_hours_1:
                    try:
                        if hour[0].isdigit():
                            hour = hour.replace('.', ':')
                            hours.append(hour)
                    except IndexError:
                        pass

                for hour in list_hours_2:
                    try:
                        if hour[0].isdigit():
                            hour = hour.replace('.', ':')
                            hours.append(hour)
                    except IndexError:
                        pass

                # преобразовываем время работы в нужный формат
                right_list_hours = [f'mon-thu {hours[0]} - {hours[1]} {hours[2]}-{hours[3]}', f'fri {hours[0]} - {hours[1]} {hours[2]}-{hours[4]}']
                city['working_hours'] = right_list_hours


        city_copy = city.copy()
        cities.append(city_copy) # помещаем словарь в общий список
        city.clear()
except IndexError:
    pass

json_cicties = json.dumps(cities)
print(json_cicties)

