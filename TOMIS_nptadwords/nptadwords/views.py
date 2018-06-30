from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Record
from .serializers import RecordSerializers
from datetime import datetime
from decimal import *


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_record(request, pk):
    try:
        record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of single record
    if request.method == 'GET':
        serializer = RecordSerializers(record)
        return Response(serializer.data)
    # delete single record
    elif request.method == 'DELETE':
        return Response({})
    # update detail of single record
    elif request.method == 'PUT':
        data = {
            'AccountDescriptiveName': request.data.get('AccountDescriptiveName'),
            'CampaignId': int(request.data.get('CampaignId')),
            'CampaignName': request.data.get('CampaignName'),
            'CampaignStatus': bool(request.data.get('CampaignStatus') == 'enabled'),
            'CityCriteriaId': int(request.data.get('CityCriteriaId')),
            'CountryCriteriaId': int(request.data.get('CountryCriteriaId')),
            'CustomerDescriptiveName': request.data.get('CustomerDescriptiveName'),
            'ExternalCustomerId': int(request.data.get('ExternalCustomerId')),
            'IsTargetingLocation': bool(request.data.get('IsTargetingLocation').lower() in ("yes", "true", "t", "1")),
            'MetroCriteriaId': request.data.get('MetroCriteriaId'),
            'MostSpecificCriteriaId': int(request.data.get('MostSpecificCriteriaId')),
            'RegionCriteriaId': int(request.data.get('RegionCriteriaId')),
            'Date': datetime.strptime(request.data.get('Date'),"%Y-%m-%d").date(),
            'Device': request.data.get('Device'),
            'LocationType': request.data.get('LocationType'),
            'AveragePosition': Decimal(request.data.get('AveragePosition')),
            'Clicks': int(request.data.get('Clicks')),
            'Conversions': Decimal(request.data.get('Conversions')),
            'ConversionValue': Decimal(request.data.get('ConversionValue')),
            'Cost': int(request.data.get('Cost')),
            'Impressions': int(request.data.get('Impressions')),
            'Interactions': int(request.data.get('Interactions')),
            'InteractionTypes': request.data.get('InteractionTypes'),
            'VideoViews': int(request.data.get('VideoViews')),
        }
        serializer = RecordSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_records(request):
    # get all records
    if request.method == 'GET':
        records = Record.objects.all()
        serializer = RecordSerializers(records, many=True)
        return Response(serializer.data)
    # insert a new record for an record
    elif request.method == 'POST':
        data = {
            'AccountDescriptiveName': request.data.get('AccountDescriptiveName'),
            'CampaignId': int(request.data.get('CampaignId')),
            'CampaignName': request.data.get('CampaignName'),
            'CampaignStatus': bool(request.data.get('CampaignStatus') == 'enabled'),
            'CityCriteriaId': int(request.data.get('CityCriteriaId')),
            'CountryCriteriaId': int(request.data.get('CountryCriteriaId')),
            'CustomerDescriptiveName': request.data.get('CustomerDescriptiveName'),
            'ExternalCustomerId': int(request.data.get('ExternalCustomerId')),
            'IsTargetingLocation': bool(request.data.get('IsTargetingLocation').lower() in ("yes", "true", "t", "1")),
            'MetroCriteriaId': request.data.get('MetroCriteriaId'),
            'MostSpecificCriteriaId': int(request.data.get('MostSpecificCriteriaId')),
            'RegionCriteriaId': int(request.data.get('RegionCriteriaId')),
            'Date': datetime.strptime(request.data.get('Date'),"%Y-%m-%d").date(),
            'Device': request.data.get('Device'),
            'LocationType': request.data.get('LocationType'),
            'AveragePosition': Decimal(request.data.get('AveragePosition')),
            'Clicks': int(request.data.get('Clicks')),
            'Conversions': Decimal(request.data.get('Conversions')),
            'ConversionValue': Decimal(request.data.get('ConversionValue')),
            'Cost': int(request.data.get('Cost')),
            'Impressions': int(request.data.get('Impressions')),
            'Interactions': int(request.data.get('Interactions')),
            'InteractionTypes': request.data.get('InteractionTypes'),
            'VideoViews': int(request.data.get('VideoViews')),
        }
        serializer = RecordSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

