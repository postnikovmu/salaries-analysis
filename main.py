import requests


def get_hh_vacancies(text):
    vacancies_url = "https://api.hh.ru/vacancies"
    params = {
        'text': text,
    }
    response = requests.get(vacancies_url, params=params)
    response.raise_for_status()
    vacancy_descriptions = response.json()
    return vacancy_descriptions


def main():
    print(get_hh_vacancies('python developer'))


if __name__ == '__main__':
    main()
