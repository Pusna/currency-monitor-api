import requests
from celery import shared_task
from django.db import transaction
from .models import Currency, RateHistory


CURRENCY_MAP = {
    840: 'USD',
    978: 'EUR',
    985: 'PLN',
    826: 'GBP',
}


@shared_task
def update_exchange_rates():

    url = "https://api.monobank.ua/bank/currency"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Помилка запиту: {str(e)}"

    tracked_currencies = Currency.objects.filter(is_tracked=True)
    if not tracked_currencies.exists():
        return "Немає валют для відстеження"

    tracked_dict = {c.code: c for c in tracked_currencies}

    updated_count = 0

    with transaction.atomic():
        for item in data:

            if item.get('currencyCodeB') == 980:
                code_a = item.get('currencyCodeA')

                if code_a in tracked_dict:
                    currency = tracked_dict[code_a]

                    rate_buy = item.get('rateBuy') or item.get('rateCross')
                    rate_sell = item.get('rateSell') or item.get('rateCross')

                    if rate_buy and rate_sell:
                        currency.current_rate_buy = rate_buy
                        currency.current_rate_sell = rate_sell
                        currency.save()

                        RateHistory.objects.create(
                            currency=currency,
                            rate_buy=rate_buy,
                            rate_sell=rate_sell
                        )
                        updated_count += 1

    return f"Оновлено курсів: {updated_count}"