from rest_framework import serializers
from .models import Currency, RateHistory


class RateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RateHistory
        fields = ['rate_buy', 'rate_sell', 'timestamp']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'is_tracked', 'current_rate_buy', 'current_rate_sell', 'last_updated']
        read_only_fields = ['code', 'name', 'current_rate_buy', 'current_rate_sell', 'last_updated']


class CurrencyTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['is_tracked']