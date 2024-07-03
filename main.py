import requests


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
    return vacancy_descriptions


def main():
    print(get_hh_vacancies('python developer'))


if __name__ == '__main__':
    main()
