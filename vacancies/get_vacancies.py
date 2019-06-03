import argparse
from terminaltables import SingleTable
from fetch_hh import fetch_headhunter_vacancies
from fetch_sj import fetch_superjob_vacancies


def print_vacancies_statistics(title, vacancies_info):

    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language, vacancie_info in vacancies_info.items():
        vacancie = []
        vacancie.append(language)
        vacancie.append(vacancie_info['vacancies_found'])
        vacancie.append(vacancie_info['vacancies_processed'])
        vacancie.append(vacancie_info['average_salary'])
        table_data.append(vacancie)

    table_instance = SingleTable(table_data, title)
    table_instance.justify_columns[1] = 'right'
    table_instance.justify_columns[2] = 'right'
    table_instance.justify_columns[3] = 'right'

    print(table_instance.table)


def main():
    parser = argparse.ArgumentParser(
       description='''Сравнение вакансий программистов на SuperJob и HeadHunter'''
    )
    parser.add_argument('days_count', help='Укажите за сколько последних дней')
    args = parser.parse_args()
    days_count = int(args.days_count)

    texts = ['Python',
             'Javascript',
             'Java',
             'Oracle',
             'PHP',
             ]

    town = '4'
    vacancies_info = fetch_superjob_vacancies(town, days_count, texts)

    print()
    title = '  SuperJob Москва  '
    print_vacancies_statistics(title, vacancies_info)

    print()

    town = '1'
    vacancies_info = fetch_headhunter_vacancies(town, days_count, texts)

    title = '  HeadHunter Москва  '
    print_vacancies_statistics(title, vacancies_info)

if __name__ == "__main__":
    main()
