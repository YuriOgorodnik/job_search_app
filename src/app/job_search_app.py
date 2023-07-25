from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional, List

from src.work.api.hh_api import HeadHunterAPI
from src.work.api.sj_api import SuperJobAPI
from src.file_handler.json_file_handler import JSONFileHandler
from src.validation.validation_vacancies import Vacancy
from src.utils.currency_converter import get_currency_data
from src.app.job_search_meta import JobSearchAppMeta


class JobSearchApp(metaclass=JobSearchAppMeta):
    __vacancies: List[Vacancy] = []
    __hh_api: HeadHunterAPI = HeadHunterAPI()
    __sj_api: SuperJobAPI = SuperJobAPI()
    __json_file_handler: JSONFileHandler = JSONFileHandler("json_vacancies.json")
    __job_title: Optional[str] = None
    __amount_vacancy: Optional[int] = None

    @classmethod
    def _user_interaction(cls) -> None:
        """
        Метод взаимодействия с пользователем.
        """
        print("ДОБРОГО ВРЕМЕНИ СУТОК, УВАЖАЕМЫЙ ПОЛЬЗОВАТЕЛЬ!!!\nВас приветствует платформа поиска вакансий для"
              " трудоустройства,\nкоторая содержит предложения популярных сайтов hh.ru и superjob.ru.")
        print("-------------------------------------------------------------------")
        cls.__job_title = input("Для поиска необходимых вакансий введите название искомой вакансии: ")
        print()
        cls.__search_vacancies()
        cls.__amount_vacancy = int(input("Введите необходимое количество найденных вакансий для отображения"
                                         " (сохранения): "))
        print()

        while True:
            print("Нажмите 1: Для сортировки найденных вакансий по дате их размещения")
            print("Нажмите 2: Для сортировки найденных вакансий по уровню заработной платы")
            print()
            choice_sorted = input("Пожалуйста, выберите критерии для сортировки, введя 1 или 2: ")
            print()
            if choice_sorted == "1":
                cls.__sorted_vacancy_for_date()
                break
            elif choice_sorted == "2":
                cls.__sorted_vacancy_for_salary()
                break
            else:
                print("Это неверный выбор. Попробуйте сново!")
        while True:
            print("Нажмите 1: Для продолжения поиска вакансий")
            print("Нажмите 2: Для отображения найденных вакансий")
            print("Нажмите 3: Для сохранения найденных вакансий в файл")
            print("Нажмите 4: Для ВЫХОДА из программы")
            print()
            choice_menu = input("Пожалуйста, сделайте Ваш выбор путем ввода необходимой цифры: ")
            print()
            if choice_menu == "1":
                cls.__job_title = input("Для поиска необходимых вакансий введите название искомой вакансии: ")
                print()
                cls.__search_vacancies()
                cls.__amount_vacancy = int(input("Введите необходимое количество найденных вакансий для отображения"
                                                 " (сохранения): "))
                print()
                while True:
                    print("Нажмите 1: Для сортировки найденных вакансий по дате их размещения")
                    print("Нажмите 2: Для сортировки найденных вакансий по уровню заработной платы")
                    print()
                    choice_sorted = input("Пожалуйста, выберите критерии для сортировки, введя 1 или 2: ")
                    print()
                    if choice_sorted == "1":
                        cls.__sorted_vacancy_for_date()
                        break
                    elif choice_sorted == "2":
                        cls.__sorted_vacancy_for_salary()
                        break
                    else:
                        print("Это неверный выбор. Попробуйте сново!")
            elif choice_menu == "2":
                cls.__display_vacancies()
            elif choice_menu == "3":
                if cls.__vacancies:
                    cls.__save_vacancies_to_file()
                    print("Найденные по запросу вакансии сохранены в файл.")
                else:
                    print("Нет найденных вакансий для сохранения.")
            elif choice_menu == "4":
                break
            else:
                print("Это неверный выбор. Попробуйте сново!")

    @classmethod
    def __search_vacancies(cls) -> None:
        """
        Метод для поиска вакансий.
        """
        with ThreadPoolExecutor() as executor:
            hh_future = executor.submit(cls.__hh_api.search_vacancies, cls.__job_title)
            sj_future = executor.submit(cls.__sj_api.search_vacancies, cls.__job_title)
            hh_vacancies = hh_future.result()
            sj_vacancies = sj_future.result()
            for vacancy_data in hh_vacancies + sj_vacancies:
                title = cls.__get_title(vacancy_data)
                link = cls.__get_link(vacancy_data)
                salary_from = cls.__get_salary(vacancy_data)
                date_published = cls.__get_date_published(vacancy_data)
                currency = cls.__get_currency(vacancy_data)
                cls.__check_currency(title, link, salary_from, date_published, currency)

        return cls.__filtered_vacancies()

    @staticmethod
    def __get_title(vacancy) -> str:
        """
        Метод для получения названия вакансии.
        """
        return vacancy["profession"] if vacancy.get("profession") is not None else vacancy["name"]

    @staticmethod
    def __get_link(vacancy) -> str:
        """
        Метод для получение ссылки на вакансию.
        """
        return vacancy["link"] if vacancy.get("link") is not None else vacancy["alternate_url"]

    @staticmethod
    def __get_salary(vacancy) -> int:
        """
        Метод для получения зарплаты по вакансии.
        """
        return vacancy["payment_from"] if vacancy.get("payment_from") is not None else vacancy["salary"]["from"]

    @staticmethod
    def __get_date_published(vacancy) -> str:
        """
        Метод для получения даты публикации вакансии.
        """
        return datetime.utcfromtimestamp(vacancy["date_published"]).strftime('%Y.%m.%d') if vacancy.get(
            "date_published") is not None else datetime.fromisoformat(vacancy["published_at"]).strftime('%Y.%m.%d')

    @staticmethod
    def __get_currency(vacancy) -> str:
        """
        Метод для получение валюты зарплаты по вакансии.
        """
        return vacancy["currency"].upper() if vacancy.get("currency") else vacancy["salary"]["currency"].upper()

    @classmethod
    def __check_currency(cls, title, link, salary, date, currency) -> None:
        """
        Метод проверки (преобразования) валюты зарплаты и добавления вакансии в список вакансий.
        """
        if currency not in ["RUR", "RUB"] and salary:
            salary *= get_currency_data(currency)
        if salary:
            cls.__vacancies.append(Vacancy(title, link, salary, date))

    @classmethod
    def __display_vacancies(cls) -> None:
        """
        Метод для отображения найденных вакансий
        """
        if cls.__vacancies:
            print("Отлично, для Вас найдены следующие вакансии:")
            print()
            [print(vacancy) for vacancy in cls.__vacancies]
        else:
            print("Нет доступных вакансий.")

    @classmethod
    def __filtered_vacancies(cls) -> None:
        """
        Метод для фильтрации вакансий по названию профессии
        """
        cls.__vacancies = list(filter(lambda x: cls.__job_title.lower() in x.title.lower() and x.salary is not None,
                                      cls.__vacancies))

    @classmethod
    def __sorted_vacancy_for_salary(cls) -> None:
        """
        Метод для сортировки вакансий по уровню зарплаты.
        """
        if cls.__amount_vacancy > len(cls.__vacancies):
            print(f"К сожалению, найдено всего {len(cls.__vacancies)} вакансий")
        cls.__vacancies = sorted(cls.__vacancies, key=lambda x: x.salary, reverse=True)[
                          :cls.__amount_vacancy]

    @classmethod
    def __sorted_vacancy_for_date(cls) -> None:
        """
        Метод для сортировки вакансий по дате их публикации.
        """
        if cls.__amount_vacancy > len(cls.__vacancies):
            print(f"К сожалению, найдено всего {len(cls.__vacancies)} вакансий")
        cls.__vacancies = sorted(cls.__vacancies, key=lambda x: x.date, reverse=True)[
                          :cls.__amount_vacancy]

    @classmethod
    def __save_vacancies_to_file(cls) -> None:
        """
        Метод для сохранения найденных по запросу вакансий в JSON-файл.
        """
        for vacancy in cls.__vacancies:
            cls.__json_file_handler.add_vacancy(vacancy)
