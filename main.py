import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


url = 'https://hh.ru/search/vacancy?area=1&area=2&text=python'

def get_headers():
    return Headers(browser="firefox", os="win").generate()

page = requests.get(url, headers=get_headers())
text = page.text
soup = BeautifulSoup(text, features='lxml')
vacancies = soup.find_all(class_="serp-item")

keywords = ['Django', 'Flask']

for vacancy in vacancies:
    # смотрим страницу со всеми вакансиями:
    vacancy_name = vacancy.find('h3').find('a')
    vacancy_url = vacancy_name.attrs['href']
    company_name = vacancy.find(class_="vacancy-serp-item__meta-info-company").find('a')
    city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary is not None:
        print(salary.text)
    else:
        print("Данные о зарплате не найдены")


    # Проверяем условия поиска:
    # for data in vacancy:
    #     page = requests.get(vacancy_url, headers=get_headers())
    #     text = page.text
    #     vacancy_soup = BeautifulSoup(text, 'html.parser')
    #     skill = soup.find(class_="bloko-tag-list")
    #     for i in skill:
    #         skill_name = skill.find('span')
    #         print(skill_name.text)



    # поиск на другой странице
    # descr = (BeautifulSoup(requests.get(links, headers=headers).text, features='lxml')).find('div', {
    #     'data-qa': 'vacancy-description'}).text

    # print(vacancy_name.text, '-->', url)


if '__name__' == '__main__':
    main()