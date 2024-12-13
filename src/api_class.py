import requests


class HHAPI:
    """Класс для получения вакансий с hh.ru"""

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self, company_name: str, page: int = 0):
        self.company_name = company_name
        self.page = page

    def get_vacancies(self):
        params = {
            "text": self.company_name,
            "area": 113,
            "per_page": 100,
            "page": self.page,
        }
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return []
