from .models import Record
from .serializers import RecordSerializers
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from chartit import PivotChart, PivotDataPool
from django.shortcuts import render
from django.db.models import Sum, Avg


class RecordList(generics.ListCreateAPIView):
    """
    API endpoint that allows records to be viewed or edited.

    get:
    List all records, ordered by date desc by default.

    post:
    Create a new record. All fields are required.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializers
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('CampaignId', 'CampaignStatus', 'Date', 'Device',
                     'LocationType', 'CityCriteriaId', 'CountryCriteriaId',
                     'MetroCriteriaId', 'MostSpecificCriteriaId',
                     'RegionCriteriaId', 'ExternalCustomerId',
                     'InteractionTypes', 'CreatedAt', 'UpdatedAt')
    search_fields = ('AccountDescriptiveName', 'CampaignName',
                     'CustomerDescriptiveName')
    ordering_fields = ('Date', 'AveragePosition', 'Clicks', 'Conversions',
                       'ConversionValue', 'Cost', 'Impressions',
                       'Interactions', 'VideoViews', 'CreatedAt', 'UpdatedAt')
    ordering = ('Date')


class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows indivdual records to be viewed or edited.

    get:
    Get one record by id.

    put:
    Update an entire record.

    patch:
    Edit a field of a record.

    delete:
    Delete a record.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializers


def homepage(request):
    ds = PivotDataPool(
        series=[
            {'options': {
                'source': Record.objects.all(),
                'categories': [
                    'Date', ],
                'legend_by': 'RegionCriteriaId',
                'top_n_per_cat': 5},
                'terms': {
                    'total_impressions': Sum('Impressions'),
                    'average_position': {
                        'func': Avg('AveragePosition'),
                        'legend_by': None}}}],
        top_n=150,
        top_n_term='total_impressions')

    pivcht = PivotChart(
        datasource=ds,
        series_options=[
            {'options': {
                'type': 'column',
                'stacking': True,
                'xAxis': 0,
                'yAxis': 0},
                'terms': ['total_impressions',
                          {'average_position': {
                           'type': 'line',
                           'yAxis': 1}}]
             }],
        chart_options={
            'title': {
                'text': 'Average Search Position, Total Impressions(lgnd. by RegionCriteriaId) vs. Date'
            },
            'yAxis': [{'title': {'text': 'Total Impressions'}}, {'opposite': True}],
            'xAxis': {
                'title': {
                    'text': 'RegionCriteriaId'
                }
            }})

    ds2 = PivotDataPool(
        series=[
            {'options': {
                'source': Record.objects.all(),
                'categories': [
                    'Date', ],
                'legend_by': 'Device'},
                'terms': {
                    'total_impressions': Sum('Impressions'),
                    'average_position': {
                        'func': Avg('AveragePosition'),
                        'legend_by': None}}}],
        top_n=150,
        top_n_term='total_impressions')

    pivcht2 = PivotChart(
        datasource=ds2,
        series_options=[
            {'options': {
                'type': 'column',
                'stacking': True,
                'xAxis': 0,
                'yAxis': 0},
                'terms': ['total_impressions',
                          {'average_position': {
                           'type': 'line',
                           'yAxis': 1}}]
             }],
        chart_options={
            'title': {
                'text': 'Average Search Position, Total Impressions(lgnd. by Device) vs. Date'
            },
            'yAxis': [{'title': {'text': 'Total Impressions'}}, {'opposite': True}],
            'xAxis': {
                'title': {
                    'text': 'Date'
                }
            }})

    return render(request, 'index.html', {
        'chart_list': [pivcht, pivcht2],
        'title': 'Pivot  Chart'
    })
