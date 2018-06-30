from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountSerializers
from datetime import datetime
from decimal import *

@api_view(['GET', 'UPDATE', 'DELETE'])
def get_delete_update_account(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of single account
    if request.method == 'GET':
        serializer = AccountSerializers(account)
        return Response(serializer.data)
    # delete single account
    elif request.method == 'DELETE':
        return Response({})
    # update detail of single account
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_accounts(request):
    # get all accounts
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializers(accounts, many=True)
        return Response(serializer.data)
    # insert a new record for an account
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
        serializer = AccountSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

