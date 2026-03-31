import csv
from django.core.management.base import BaseCommand
from apps.currencies.models import Currency


class Command(BaseCommand):
    help = 'Створює CSV-файл зі списком валют та їх поточним курсом'

    def handle(self, *args, **options):
        filename = 'currencies_export.csv'

        currencies = Currency.objects.all()

        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Code', 'Is Tracked', 'Buy Rate', 'Sell Rate', 'Last Updated'])

            for curr in currencies:
                writer.writerow([
                    curr.id,
                    curr.name,
                    curr.code,
                    curr.is_tracked,
                    curr.current_rate_buy or 'N/A',
                    curr.current_rate_sell or 'N/A',
                    curr.last_updated.strftime('%Y-%m-%d %H:%M:%S')
                ])

        self.stdout.write(self.style.SUCCESS(f'Успішно експортовано дані у файл: {filename}'))