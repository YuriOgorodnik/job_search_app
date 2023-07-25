Проект "Job Search App": Поиск вакансий по API с сайтов hh.ru и superjob.ru

Авторство: Огородник Юрий Александрович.

Назначение проекта: Проект "Job Search App": - это приложение для поиска и обработки вакансий из различных API. Пользователь может выполнять поиск вакансий, отображать результаты, сохранять вакансии в файл.

Программное обеспечение, библиотеки:

    Язык программирования: Python (3.7 и выше);
    Библиотеки: certifi, charset-normalizer, dbf-light, idna, pycbrf, requests, urllib3.

Класс JobSearchApp представляет основное приложение для выполнения операций по поиску и обработке вакансий.
Методы класса:

    __init__(self): Инициализирует объект JobSearchApp.
    __user_interaction(cls): Обеспечивает взаимодействие с пользователем и обработку его выбора.
    __search_vacancies(self): Выполняет поиск вакансий.
    __get_title(vacancy): Получает название вакансии.
    __get_link(vacancy): Получает ссылку на вакансию.
    __get_salary(vacancy): Получает зарплату по вакансии.
    __get_date_published(vacancy): Получает дату публикации вакансии.
    __get_currency(vacancy): Получает валюту вакансии.
    __check_currency(title, link, salary, date, currency): Проверяет валюту и преобразует зарплату.
    __display_vacancies(cls): Отображает найденные вакансии.
    __filtered_vacancies(cls): Фильтрует вакансии по названию профессии.
    __sorted_vacancy_for_salary(cls): Сортирует вакансии по зарплате.
    __sorted_vacancy_for_date(cls): Сортирует вакансии по дате публикации.
    __save_vacancies_to_files(cls): Сохраняет вакансии в файл JSON.

Установка и использование проекта:

    Скачайте исходный код с GitHub;
    Установите зависимости, запустите pip install -r requirements.txt;
    Запустите проект с помощью команды python main.py