import requests
from bs4 import BeautifulSoup

URL = 'https://tlgrm.ru/channels/news'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           'accept': '*/*'}

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='channel-card ')

    channels = []
    for item in items:
        channels.append({
            'title': item.find('h3', class_='channel-card__title').get_text(strip=True)
        })
    print(channels)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('error')

parse()
