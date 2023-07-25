import json
from typing import Dict, Any, List

from src.file_handler.base_file_handler import BaseFileHandler, Vacancy


class JSONFileHandler(BaseFileHandler):
    """
    Класс для обработки информации в JSON-файле с вакансиями
    """

    def __init__(self, file_path: str):
        """
         Инициализация класса JSONFileHandler.

        :param file_path: Путь к JSON-файлу.
        """
        self.file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод добавления найденной вакансии в JSON-файл.

        :param vacancy: Вакансия для добавления.
        """
        with open(self.file_path, "a", encoding="utf-8") as file:
            vacancy_dict = {
                "title": vacancy.title,
                "link": vacancy.link,
                "salary": vacancy.salary,
                "date": vacancy.date
            }
            json.dump(vacancy_dict, file, ensure_ascii=False)
            file.write("\n")

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Метод, возвращающий список вакансий из JSON-файла, которые соответствуют заданным критериям.

        :param criteria: Критерии для выборки вакансий.
        :return: Список вакансий, соответствующих заданным критериям.
        """
        vacancies = []
        with open(self.file_path, "r") as file:
            for line in file:
                vacancy_data = json.loads(line)
                if self._vacancy_matches_criteria(vacancy_data, criteria):
                    vacancies.append(vacancy_data)
        return vacancies

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод для удаления вакансии из JSON-файла.

        :param vacancy: Вакансия для удаления.
        """
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        with open(self.file_path, "w") as file:
            for line in lines:
                vacancy_data = json.loads(line)
                if not self._vacancy_equals(vacancy_data, vacancy):
                    file.write(line)

    @staticmethod
    def _vacancy_matches_criteria(vacancy_data: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Метод для проверки соответствия вакансии заданным критериям.

        :param vacancy_data: Данные по вакансии.
        :param criteria: Критерии для проверки.
        :return: Если вакансия соответствует критериям, то True, иначе - False.
        """
        for key, value in criteria.items():
            if key not in vacancy_data or vacancy_data[key] != value:
                return False
        return True

    @staticmethod
    def _vacancy_equals(vacancy_data1: Dict[str, Any], vacancy_data2: Dict[str, Any]) -> bool:
        """
        Метод для проверки соответствия двух найденных вакансий.

        :param vacancy_data1: Данные первой вакансии.
        :param vacancy_data2: Данные второй вакансии.
        :return: Если вакансии равны, то True, иначе - False.
        """
        return vacancy_data1 == vacancy_data2
