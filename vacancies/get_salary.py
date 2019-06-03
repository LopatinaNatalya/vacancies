def predict_rub_salary(salary):
    rub_salary = None
    if salary is not None and salary['currency'] in ('RUR', 'rub'):
        salary_from = salary['from']
        salary_to = salary['to']

        if (salary_from is None and salary_to is None) or (not salary_from and not salary_to):
            rub_salary = None
        elif salary_from is None or not salary_from:
            rub_salary = salary_to*0.8
        elif salary_to is None or not salary_to:
            rub_salary = salary_from * 1.2
        else:
            rub_salary = (salary_from + salary_to)/2
    return rub_salary


def get_mean(numbers):
    return int(sum(numbers) / len(numbers)) if len(numbers) != 0 else 0
