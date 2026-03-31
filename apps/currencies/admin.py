from django.contrib import admin
from .models import Currency, RateHistory

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_tracked', 'current_rate_buy', 'current_rate_sell', 'last_updated')
    list_filter = ('is_tracked',)
    search_fields = ('name', 'code')
    list_editable = ('is_tracked',)

@admin.register(RateHistory)
class RateHistoryAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate_buy', 'rate_sell', 'timestamp')
    list_filter = ('currency', 'timestamp')
    readonly_fields = ('timestamp',)