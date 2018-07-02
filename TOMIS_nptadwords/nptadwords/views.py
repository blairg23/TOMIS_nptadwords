from .models import Record
from .serializers import RecordSerializers
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


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
