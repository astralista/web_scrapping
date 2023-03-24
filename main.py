import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import time

keywords = ['Django', 'Flask']

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def get_links(text):
    data = requests.get(
        url=f'https://hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text={text}&page=1',
        headers=get_headers()
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')

    # если надо будет обойти все страницы поиска
    # используй page_count в range цикла ниже:
    # try:
    #     page_count = int(soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    # except:
    #     return

    for page in range(2):
        try:
            data = requests.get(
                url=f'https://hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text={text}&page={page}',
                headers=get_headers()
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all('a', attrs={'class': 'serp-item__title'}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f'{e}')
        time.sleep(1)
def get_vacancy(link):
    data = requests.get(
        url=link,
        headers=get_headers()
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    # ищем тэги
    try:
        tags = [tag.text for tag in soup.find(attrs={'class': 'bloko-tag-list'}).find_all(attrs={'class': 'bloko-tag__section_text'})]
    except:
        tags = []

    for tag in tags:
        for keyword in keywords:
            if keyword.lower() == tag.lower():
                # если ключи совпали, добавляем данные
                try:
                    # название компании
                    name = soup.find('div', attrs={'class': 'vacancy-company-details'}).text.replace('\xa0', ' ')
                except:
                    name = ''
                try:
                    # ветка зарплат
                    salary = soup.find(attrs={'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text.replace('\xa0', ' ')
                except:
                    salary = ''
                try:
                    # город
                    city = soup.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
                except:
                    city = ''

                vacancy = {
                    'link': link,
                    'salary': salary,
                    'name': name,
                    'city': city
                }
                return vacancy
    return None


if __name__ == '__main__':
    data = []
    for i in get_links('python'):
        vacancy = get_vacancy(i)
        if vacancy is not None:
            data.append(vacancy)
        time.sleep(1)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)