from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Currency


class CurrencyApiTests(APITestCase):
    def setUp(self):
        self.usd = Currency.objects.create(
            code=840,
            name="USD",
            is_tracked=True,
            current_rate_buy=41.50,
            current_rate_sell=42.10
        )
        self.eur = Currency.objects.create(
            code=978,
            name="EUR",
            is_tracked=False
        )

    def test_get_tracked_currencies(self):
        url = reverse('currency-tracked')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['code'], 840)

    def test_get_available_currencies(self):
        """Перевірка списку доступних валют"""
        url = reverse('currency-available')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Має бути EUR
        self.assertEqual(response.data[0]['code'], 978)

    def test_toggle_tracking_status(self):
        """Перевірка PATCH методу"""
        url = reverse('currency-toggle-tracking', kwargs={'pk': self.eur.pk})
        response = self.client.patch(url, {'is_tracked': True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.eur.refresh_from_db()
        self.assertTrue(self.eur.is_tracked)

    def test_export_csv_endpoint(self):
        """Перевірка CSV"""
        url = reverse('currency-export-csv')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')