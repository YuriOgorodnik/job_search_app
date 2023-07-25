import requests
from src.work.api.base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """
    Класс для поиска вакансий на HeadHunter API
    """

    url: str = 'https://api.hh.ru/vacancies'

    def __init__(self, url: str = url):
        """
        Инициализация класса HeadHunterAPI.

        :param url: URL для запроса к HeadHunter API.
        """
        super().__init__(url)

    def search_vacancies(self, job_title: str) -> list:
        """
        Метод для поиска вакансий на HeadHunter API.

        :param job_title: Название вакансии для поиска.
        :return: Список найденных вакансий по запросу.
        """
        params = {
            'text': job_title,
            'per_page': self._number_of_vacancies,
            'only_with_salary': True
        }

        response = requests.get(url=self._base_url, params=params)
        response_json = response.json()

        return response_json.get("items", [])
