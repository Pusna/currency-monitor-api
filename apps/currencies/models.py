from django.db import models


class Currency(models.Model):
    code = models.IntegerField(unique=True, verbose_name="Код ISO")
    name = models.CharField(max_length=10, verbose_name="Назва")
    is_tracked = models.BooleanField(default=False, verbose_name="Відстежується")

    current_rate_buy = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Поточна купівля"
    )
    current_rate_sell = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Поточний продаж"
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюти"

    def __str__(self):
        return f"{self.name} ({self.code})"


class RateHistory(models.Model):
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name='history', verbose_name="Валюта"
    )
    rate_buy = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Курс купівлі")
    rate_sell = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Курс продажу")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Час запису")

    class Meta:
        verbose_name = "Історія"
        verbose_name_plural = "Історії"
        ordering = ['-timestamp']