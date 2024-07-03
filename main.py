import requests
import time


def get_hh_vacancies(text):
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
        page += 1
        time.sleep(0.5)
    return all_vacancies, vacancy_descriptions['found']


def fetch_hh_programmers(languages):
    vacancies_hh = {}
    delay_time = 0.5

    for language in languages:
        vacancies, total_vacancies = get_hh_vacancies(language)
        vacancies_hh[language] = total_vacancies
        time.sleep(delay_time)

    return vacancies_hh


def main():

    languages = [
        'Python', 'Java', 'C++', 'JavaScript', 'C#', 'Swift', 'Kotlin', 'Ruby', 'PHP', 'Go'
    ]
    print(fetch_hh_programmers(languages))


if __name__ == '__main__':
    main()
