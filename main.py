import requests
from bs4 import BeautifulSoup

url = 'https://www.papajohns.com/order/specials/index.html'
response = requests.get(url)

with open('dominos.html', 'w') as file:
    file.write(response.text)

soup = BeautifulSoup(response.text, 'lxml')