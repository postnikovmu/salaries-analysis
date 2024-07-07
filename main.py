import os
import requests
import time
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_hh_vacancies(text, page_limit):
    vacancies_url = "https://api.hh.ru/vacancies"
    area_id = '1'
    vacancies_per_page = '100'
    params = {
        'text': text,
        'area': area_id,
        'per_page': vacancies_per_page,
    }
    all_vacancies = []
    page = 0
    while True:
        params['page'] = page
        response = requests.get(vacancies_url, params=params)
        response.raise_for_status()
        vacancy_descriptions = response.json()
        all_vacancies.extend(vacancy_descriptions['items'])
        if page >= vacancy_descriptions['pages'] - 1:
            break
        if page >= page_limit:
            break
        page += 1
        time.sleep(0.5)
    return all_vacancies, vacancy_descriptions['found']


def fetch_hh_programmers(languages, page_limit=1000):
    vacancies_hh = {}
    delay_time = 0.5

    for language in languages:
        vacancies, vacancies_found = get_hh_vacancies(language, page_limit)
        vacancies_processed = 0
        total_salary = 0
        for v in vacancies:
            salary = v.get('salary')
            predicted_salary = predict_rub_salary(salary)
            if predicted_salary:
                vacancies_processed += 1
                total_salary += predicted_salary
        average_salary = int(total_salary / vacancies_processed)
        salaries = {'vacancies_found': vacancies_found,
                    'vacancies_processed': vacancies_processed,
                    'average_salary': average_salary,
                    }

        vacancies_hh[language] = salaries
        time.sleep(delay_time)

    return vacancies_hh


def get_superjob_vacancies(language, api_key):
    vacancies_url = "https://api.superjob.ru/2.0/vacancies/"
    start_page_number = 0
    vacancies_per_page = 100
    city_name = 'Москва'
    headers = {'X-Api-App-Id': api_key}
    params = {
        'page': start_page_number,
        'count': vacancies_per_page,
        'town': city_name,
        'keyword': language
    }

    all_vacancies = []

    page = 0
    while True:
        params['page'] = page
        response = requests.get(vacancies_url, headers=headers, params=params)
        response.raise_for_status()

        vacancy_descriptions = response.json()
        all_vacancies.extend(vacancy_descriptions['objects'])
        if len(all_vacancies) >= vacancy_descriptions['total']:
            break
        page += 1
        time.sleep(0.5)
    return all_vacancies, vacancy_descriptions['total']


def fetch_sj_programmers(api_key, languages):
    vacancies_superjob_salaries = {}
    delay_time = 0.5

    for language in languages:
        vacancies, total_vacancies = get_superjob_vacancies(language, api_key)
        salaries = []
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
            if predicted_salary:
                salaries.append(predicted_salary)
        average_salary = int(sum(salaries) / len(salaries)) if salaries else 0
        vacancies_superjob_salaries[language] = {
            'vacancies_found': total_vacancies,
            'vacancies_processed': len(salaries),
            'average_salary': average_salary,
        }
        time.sleep(delay_time)

    return vacancies_superjob_salaries


def predict_rub_salary(salary):
    if not salary or salary['currency'] != 'RUR':
        return None
    predicted_salary = 0

    payment_from = salary.get('from')
    payment_to = salary.get('to')
    if payment_from and payment_to:
        predicted_salary = (payment_from + payment_to) / 2
    elif payment_from:
        predicted_salary = payment_from * 1.2
    elif payment_to:
        predicted_salary = payment_to * 0.8

    return predicted_salary


def print_table(vacancy_descriptions, title):
    table_columns = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, stats in vacancy_descriptions.items():
        table_columns.append(
            [language, stats['vacancies_found'], stats['vacancies_processed'], stats['average_salary']])
    table = AsciiTable(table_columns, title)
    print(table.table)


def main():

    load_dotenv()
    api_key = os.getenv('SUPER_JOB_KEY')

    languages = [
        'Python', 'Go', 'JavaScript', 'C++', 'Java', 'C#', 'Kotlin', 'Swift', 'Ruby', 'PHP',
    ]

    hh_programmers_salaries = fetch_hh_programmers(languages)
    print_table(hh_programmers_salaries, "HeadHunter Moscow")

    sj_programmers_salaries = fetch_sj_programmers(api_key, languages)
    print_table(sj_programmers_salaries, "SuperJob Moscow")


if __name__ == '__main__':
    main()
