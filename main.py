import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
r = http.request('GET', 'https://oriencoop.cl/sucursales.htm')
soup = BeautifulSoup(r.data, 'lxml')
print(soup.title)
print(soup.title.text)
