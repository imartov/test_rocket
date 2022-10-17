import sys
from bs4 import BeautifulSoup
import requests
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd

url = 'https://oriencoop.cl/sucursales/165'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

for map_ in soup.find_all('iframe'):
    scr_ = str(map_.get('src'))
    html_text_scr = requests.get(scr_).text
    soup_scr = BeautifulSoup(html_text_scr, 'lxml')
    print(soup_scr)






'''
oriencoop_name = soup.title.string[11:]

phones_ = []
phones = soup.find('div', class_ = 'b-call shadow').text
phones = phones.split('\n')
for value in phones:
    try:
        if value[1].isdigit():
            phones_.append(value)
    except IndexError:
        pass

list_links = []
for link in soup.find_all('a'):
    try:
        if 'sucursales' in link.get('href'):
            link = 'https://oriencoop.cl/' + link.get('href')
            list_links.append(link)
    except TypeError:
        pass

cities = []
city = {}
for idx_city, link in enumerate(list_links[1:-1]):
    html_text_link = requests.get(link).text
    soup_link = BeautifulSoup(html_text_link, 'lxml')
    direction = soup_link.find('div', 's-dato').text
    for idx, value in enumerate(direction):
        if value == 'Dirección:':
            city['address'] = direction[idx + 1]
            city['name'] = oriencoop_name
        elif value == 'Teléfono:':
            city['phones'] = [direction[idx + 1]] + phones_
        elif value == 'Horarios:':
            list_hours_1 = direction[idx + 1].split()
            list_hours_2 = direction[idx + 2].split()
            hours = []
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

            right_list_hours = [f'mon-thu {hours[0]} - {hours[1]} {hours[2]}-{hours[3]}', f'fri {hours[0]} - {hours[1]} {hours[2]}-{hours[4]}']
            city['working_hours'] = right_list_hours


    city_copy = city.copy()
    cities.append(city_copy)
    cities.append('\n')
    city.clear()
    if idx_city == 2:
        break

print(cities)
'''




