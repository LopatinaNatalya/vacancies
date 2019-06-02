import requests, get_salary
from pprint import pprint


def get_vacancies_info_page(text, town, days_count, page):
    url = 'https://api.hh.ru/vacancies?text="{}"&area={}&period={}&page={}&per_page=100'.format(text, town, days_count, page)
    responses = requests.get(url)
    salary = []
    if responses.ok:
        for item in responses.json()['items']:
            rub_salary = get_salary.predict_rub_salary(item['salary'])
            if rub_salary is not None:
                salary.append(rub_salary)
    return salary, responses.json()['found'], responses.json()['pages']


def get_vacancies_info(text, town='1', days_count='2'):
    page = '0'

    salary, vacancies_found, pages = get_vacancies_info_page(text, town, days_count, page)

    for page in range(1, pages):
        sub_salary, sub_vacancies_found, sub_pages = get_vacancies_info_page(text, town, days_count, page)
        salary += sub_salary

    return vacancies_found, len(salary), get_salary.get_mean(salary)

def fetch_headhunter_vacancies(town, days_count, texts):
    vacancies_info = {}
    for text in texts:
        vacancies_found, vacancies_processed, average_salary  = get_vacancies_info(text, town, days_count)
        vacancies_info['{}'.format(text)] = {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": vacancies_processed,
                    "average_salary": average_salary
         }
    return vacancies_info

def main():
    town = '1'
    days_count = '10'
    texts = ['Python',
             'Javascript',
             'Java',
             'Oracle',
             'PHP',
             ]
    vacancies_info = fetch_headhunter_vacancies(town, days_count, texts)
    pprint(vacancies_info)

if __name__ == "__main__":
    main()