import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

HOST = 'https://hh.ru/'

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def get_vacancy_list():
    uri = f'{HOST}search/vacancy'
    params = {
        'text': ['Python','Django','Flask'],
        'area': [1, 2],
        'currency_code': None
    }
    return requests.get(uri,headers=get_headers(),params=params).text

# ключевики для поиска по критерию:
keywords = ('Django', 'Flask')

def parsing_vacancy():
    soup = BeautifulSoup(get_vacancy_list(), features='lxml')
    all_vac = soup.find('div', class_='vacancy-serp-content')
    vacancy_list = soup.find_all('div', class_='vacancy-serp-item__layout')
    got_it = []

    for vacancy in vacancy_list:
        try:
            vacancy_description = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
        except AttributeError:
            continue

        if set(keywords).issubset(vacancy_description.split()):
            city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            link_search = vacancy.find('a', class_='serp-item__title')
            link = link_search['href']
            company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
            try:
                salary = vacancy.find('span', class_='bloko-header-section-3').text.replace('\u202f', ' ')
            except AttributeError:
                continue
            vacancy_info = {
                'link': link,
                'salary': salary,
                'company': company,
                'city': city
            }
            got_it.append(vacancy_info)
        return got_it

if __name__ == '__main__':
    write_it = parsing_vacancy()
    with open('write_it.json', 'w', encoding='utf-8') as outfile:
        json.dump(write_it, outfile, ensure_ascii=False, indent=4)
