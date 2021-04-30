import requests
import json
from config import keys, API_key, url


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'{url}?access_key={API_key}&symbols={quote_ticker}')
        r1 = requests.get(f'{url}?access_key={API_key}&symbols={base_ticker}')
        if base_ticker == "EUR":
            total_base = json.loads(r.content)['rates'][quote_ticker] * amount

        else:
            A = json.loads(r1.content)['rates'][base_ticker]
            B = json.loads(r.content)['rates'][quote_ticker]
            total_base = (B / A) * amount

        return round(total_base, 2)
