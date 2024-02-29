import requests
import bs4
import fake_headers
import json
from pprint import pprint

headers = fake_headers.Headers(browser='firefox', os='win')
headers_dict = headers.generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_dict)
main_html_data = response.text
main_html = bs4.BeautifulSoup(main_html_data, "lxml")

vacancy = main_html.find('div', id="a11y-main-content")

vacancies = main_html.find_all(class_='serp-item')
parsed_data =[]
for vacancy in vacancies:
    city_tag = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    vacancy_tag = vacancy.find('a', class_='serp-item__title')
    company_tag = vacancy.find('a', class_="bloko-link bloko-link_kind-tertiary")
    link_tag = vacancy.find('a', class_="serp-item__title")
    if vacancy.find('span', class_='bloko-header-section-3'):
        salary = vacancy.find('span', class_='bloko-header-section-3').get_text()
        parsed_data.append({'link': link, 'company_name': name, 'city_name': city, 'salary': salary})
    else:
        vacancy_name = vacancy_tag.text
        name = company_tag.text
        link = f"{link_tag['href']}"
        city = city_tag.text
        parsed_data.append({'link': link, 'company_name': name, 'city_name': city})

pprint(parsed_data)

with open('vacancy.json', 'w', encoding='utf8') as outfile:
    json.dump(parsed_data, outfile, ensure_ascii=False)







