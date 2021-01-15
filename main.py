import requests
from bs4 import BeautifulSoup
from nurbaBot.setting import HEADERS


URL_russia_cinema = 'http://www.cinema.kg/'


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_dates(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    items = soup.find_all('div', class_='tab')

    dates = []

    i = 0
    for item in items:
        dates.append({
            'date': item.get_text(strip=True),
            'date_number': i                    # Что бы было легче парсить (строка 42)
        })

        i += 1

    return dates


def get_movies(date):
    response = requests.get('http://www.cinema.kg/', headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    items = soup.find_all('div', class_='tTable')

    article_info = []

    i = 0
    for item in items:
        if i == date:
            title = item.find_all('tr', class_='tRow')

            for tit in title:
                to = tit.find_all('td')
                article_info.append({
                    'date': i,
                    'time': to[0].get_text(strip=True),
                    'title': to[1].get_text(strip=True),
                    'room': to[2].get_text(strip=True),
                    'price': to[3].get_text(strip=True)
                })
        i += 1
    return article_info


print(get_dates(get_html(URL_russia_cinema)))