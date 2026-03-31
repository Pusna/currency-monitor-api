from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Currency
from rest_framework.authentication import SessionAuthentication
from .serializers import CurrencySerializer, RateHistorySerializer, CurrencyTrackSerializer
import csv
from django.http import HttpResponse


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для роботи з валютами.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @action(detail=False, methods=['get'])
    def tracked(self, request):
        currencies = self.queryset.filter(is_tracked=True)
        serializer = self.get_serializer(currencies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        currencies = self.queryset.filter(is_tracked=False)
        serializer = self.get_serializer(currencies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], serializer_class=CurrencyTrackSerializer)
    def toggle_tracking(self, request, pk=None):
        currency = self.get_object()
        serializer = self.get_serializer(currency, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        currency = self.get_object()

        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        history = currency.history.all()

        if start_date:
            history = history.filter(timestamp__date__gte=start_date)
        if end_date:
            history = history.filter(timestamp__date__lte=end_date)

        serializer = RateHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="currencies_export.csv"'

        writer = csv.writer(response)

        writer.writerow(['ID', 'Name', 'Code', 'Is Tracked', 'Buy Rate', 'Sell Rate', 'Last Updated'])

        currencies = Currency.objects.all()
        for curr in currencies:
            writer.writerow([
                curr.id,
                curr.name,
                curr.code,
                curr.is_tracked,
                curr.current_rate_buy or 'N/A',
                curr.current_rate_sell or 'N/A',
                curr.last_updated.strftime('%Y-%m-%d %H:%M:%S') if curr.last_updated else 'N/A'
            ])

        return response