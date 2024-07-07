import requests
import time


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
        average_salary = 0
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


def main():

    languages = [
        'Python', 'Java', 'C++', 'JavaScript', 'C#', 'Swift', 'Kotlin', 'Ruby', 'PHP', 'Go'
    ]
    print(fetch_hh_programmers(languages))


if __name__ == '__main__':
    main()
