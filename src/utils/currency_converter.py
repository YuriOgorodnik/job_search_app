from pycbrf import ExchangeRates
from datetime import datetime
from decimal import Decimal


def get_currency_data(currency: str) -> Decimal:
    """
    Метод получения данных о курсе заданной валюты.

    :param currency: Код другой валюты ('USD', 'EUR' и т.д.).
    :return: Курс заданной валюты относительно рубля.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    rates = ExchangeRates(current_date)
    currency = _check_currency(currency)
    currency_data = list(filter(lambda el: el.code == currency, rates.rates))[0].rate
    return Decimal(currency_data)


def _check_currency(currency: str) -> str:
    """
    Метод проверки кода валюты и возвращения его в нужном формате.

    :param currency: Код валюты.
    :return: Код валюты в нужном формате.
    """
    if currency == "BYR":
        return "BYN"
    return currency
