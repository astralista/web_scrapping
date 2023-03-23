import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import csv

url = 'https://hh.ru/search/vacancy?area=1&area=2&text=python'

def get_headers():
    return Headers(browser="firefox", os="win").generate()

# Идем на страницу поиска и выбираем блоки с описанием вакансии:
page = requests.get(url, headers=get_headers())
text = page.text
soup = BeautifulSoup(text, features='lxml')
vacancies = []

# ключевики для поиска по критерию:
keywords = ['Django', 'Flask']

# обходим блоки с вакансиями для фильтрации:
for vacancy in soup.find_all(class_="serp-item"):
    # смотрим страницу со всеми вакансиями:
    vacancy_name = vacancy.find('h3').find('a')
    vacancy_url = vacancy_name.attrs['href']
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    company_name = vacancy.find(class_="vacancy-serp-item__meta-info-company").find('a').text
    city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

    # идем на страницу вакансии:
    page_vacancy = requests.get(vacancy_url, headers=get_headers())
    vac_text = page_vacancy.text
    vacancy_soup = BeautifulSoup(vac_text, 'lxml')

    vacancy_info = {}
    # применяем ключи для фильтрации:
    if all(keyword.lower() in vacancy_soup.text.lower() for keyword in keywords):
        vacancy_info['link'] = vacancy_url
        vacancy_info['salary'] = salary.text
        vacancy_info['company'] = company_name
        vacancy_info['city'] = city
        vacancies.append(vacancy_info)

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

with open('vacancies.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Link', 'Salary', 'Company', 'City'])
    for vacancy in vacancies:
        writer.writerow([vacancy['link'], vacancy['salary'], vacancy['company'], vacancy['city']])

if '__name__' == '__main__':
    main()
