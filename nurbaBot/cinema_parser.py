import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

from nurbaBot.setting import HEADERS


def get_html(url):
    URL = url
    response = requests.get(URL, headers=HEADERS)
    return BeautifulSoup(response.content, 'html.parser')


def get_cinema_address(url):
    address = get_html(url).find('table', class_='theaterInfo_list')
    address2 = address.find('span', class_='link_border').get_text(strip=True)

    call_number = get_html(url).find('span', class_='theaterInfo_phone').get_text(strip=True)

    art_address = {
        'address': address2,
        'cell_number': call_number
    }

    return art_address


driver = webdriver.Chrome()
driver.get('https://cinematica.kg/cinema/1')


def get_cinematica():
    button = driver.find_element_by_xpath('//*[@id="root"]/div/div[5]/div/div/div[5]/div[1]/div[2]/button[5]')
    button.click()
    sleep(15)

    names = driver.find_elements_by_class_name('movie-name')

    for name in names:
        print(name.find_element_by_tag_name('span'))


def get_broadwey():
    buttons = driver.find_elements_by_class_name('uk-margin-small-bottom')

    i = 0
    for button in buttons:
        if i == 3:
            button.click()
            break
        else:
            i += 1
    sleep(1)
    elements = driver.find_elements_by_class_name('uk-text-left')

    exemple = []
    for element in elements:
        exemple.append(element.find_element_by_tag_name('li').text)

    return exemple


get_cinematica()