from bs4 import BeautifulSoup
import requests
import json

import parser
from selenium import webdriver

# перевод с русского на английский
from translate import Translator
translator = Translator(from_lang="russian", to_lang="eng")
translation = translator.translate("Россия, г. Москва, Ленинградское шоссе, д. 16А, строение 8")
print(translation)

# получение координат из адресса
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="find_coordinate")
location = geolocator.geocode(translator.translate(translation))

list_ = [location.latitude, location.longitude]

print(list_)

