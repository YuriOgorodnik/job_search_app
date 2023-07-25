import requests
import os
from src.work.api.base_api import BaseAPI


class SuperJobAPI(BaseAPI):
    """
    Класс для поиска вакансий на SuperJob API
    """

    url: str = "https://api.superjob.ru/2.0"

    def __init__(self, url: str = url):
        """
        Инициализация класса SuperJobAPI.

        :param url: URL для запроса к SuperJob API.
        """
        super().__init__(url)

    @staticmethod
    def authorization(self):
        """
        Метод для авторизации на сервисе SuperJob
        """
        response = requests.get(
            url=f'https://api.superjob.ru/2.0/oauth2/password/',
            headers={
                "X-Api-App-Id": os.getenv("API_SUPERJOB_KEY")
            },
            params={
                'login': os.getenv("API_SUPERJOB_LOGIN"),
                'password': os.getenv("API_SUPERJOB_PASSWORD"),
                'client_id': '2691',
                'client_secret': os.getenv("API_SUPERJOB_KEY")
            }
        )
        print(response.text)

    def search_vacancies(self, job_title: str) -> list:
        """
        Метод для поиска вакансий на SuperJob API.

        :param job_title: Название вакансии для поиска.
        :return: Список найденных вакансий по запросу.
        """
        url = f"{self._base_url}/vacancies/"
        headers = {
            "X-Api-App-Id": os.getenv("API_SUPERJOB_KEY")
        }
        params = {
            "keywords": [[1, job_title]],
            "count": self._number_of_vacancies,
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        return data.get("objects", [])
