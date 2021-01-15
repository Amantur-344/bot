import requests
from bs4 import BeautifulSoup
from nurbaBot.setting import HEADERS


URL_russia_cinema = 'https://cinematica.kg/cinema'


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_date(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    items = soup.find_all('div', class_='cinemalist_title')

    dates = []

    for item in items:
        dates.append(item.find('p').get_text(strip=True))

    return dates

print(get_date(get_html(URL_russia_cinema)))