import requests
import time


def get_hh_vacancies(text):
    vacancies_url = "https://api.hh.ru/vacancies"
    area_id = '1'  # id for Moscow city
    params = {
        'text': text,
        'area': area_id,
    }
    response = requests.get(vacancies_url, params=params)
    response.raise_for_status()
    vacancy_descriptions = response.json()
    return vacancy_descriptions['items']


def fetch_hh_programmers(languages):
    vacancies_hh = {}
    delay_time = 0.5

    for language in languages:
        vacancies = get_hh_vacancies(language)
        vacancies_hh[language] = len(vacancies)
        time.sleep(delay_time)

    return vacancies_hh


def main():

    languages = [
        'Python', 'Java', 'C++', 'JavaScript', 'C#', 'Swift', 'Kotlin', 'Ruby', 'PHP', 'Go'
    ]
    print(fetch_hh_programmers(languages))


if __name__ == '__main__':
    main()
