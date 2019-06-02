import requests, datetime, os, get_salary
from pprint import pprint
from dotenv import load_dotenv


def get_petiod_timestamp(days_count=1):
    date_published_to = datetime.datetime.now()
    date_published_from = date_published_to - datetime.timedelta(days=days_count)
    date_published_from = datetime.datetime(date_published_from.year, date_published_from.month, date_published_from.day, 0, 0, 0)

    return date_published_from.timestamp(), date_published_to.timestamp()

def get_vacancies_info(text, town, secret_key, days_count='1'):
    salary = []
    total = 0
    date_published_from, date_published_to = get_petiod_timestamp(days_count)

    url_api = 'https://api.superjob.ru/2.0/vacancies/'

    per_page = 100
    page = 0

    search_params = {
        'keyword': 'программист {}'.format(text),
        'town': town,
        'no_agreement': 0,
        'date_published_from' : date_published_from,
        'date_published_to' : date_published_to,
        'count': per_page,
        'page': page,
    }

    headers = {
        'X-Api-App-Id': secret_key,
    }

    for page in range(0, 501):
        search_params.update({'page': page})
        responses = requests.get(url_api, headers=headers, params=search_params)

        if responses.ok:
            total = responses.json()['total']
            for item in responses.json()['objects']:

                payment = {
                'currency': item['currency'],
                'from' : item['payment_from'],
                'to' : item['payment_to'],
                }

                rub_salary = get_salary.predict_rub_salary(payment)
                if rub_salary is not None:
                    salary.append(rub_salary)
        if not responses.json()['more']:
            break

    return total, len(salary), get_salary.get_mean(salary)

def fetch_superjob_vacancies(town, days_count, texts):
    load_dotenv()
    secret_key = os.getenv("SJ_KEY")

    vacancies_info = {}
    for text in texts:
        vacancies_found, vacancies_processed, average_salary  = get_vacancies_info(text, town, secret_key, days_count)
        vacancies_info['{}'.format(text)] = {
                     "vacancies_found": vacancies_found,
                     "vacancies_processed": vacancies_processed,
                     "average_salary": average_salary
         }

    return vacancies_info


def main():
    town = '4'
    days_count = 10
    texts = ['Python',
             'Javascript',
             'Java',
             'Oracle',
             'PHP',
             ]

    vacancies_info = fetch_superjob_vacancies(town, days_count, texts)
    pprint(vacancies_info)

if __name__ == "__main__":
    main()