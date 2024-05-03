import requests
from bs4 import BeautifulSoup

url = 'https://www.dominos.ca/en/pages/order/#!/section/Coupons/category/All/?localCoupons=true'
response = requests.get(url)

with open('dominos.html', 'w') as file:
    file.write(response.text)

soup = BeautifulSoup(response.text, 'lxml')