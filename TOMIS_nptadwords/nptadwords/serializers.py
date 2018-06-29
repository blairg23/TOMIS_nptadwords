from rest_framework import serializers
from .models import Account


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('AccountDescriptiveName', 'CampaignId', 'CampaignName',
                  'CampaignStatus', 'CityCriteriaId', 'CountryCriteriaId',
                  'CustomerDescriptiveName', 'ExternalCustomerId',
                  'IsTargetingLocation', 'MetroCriteriaId',
                  'MostSpecificCriteriaId', 'RegionCriteriaId', 'Date',
                  'Device', 'LocationType', 'AveragePosition', 'Clicks',
                  'Conversions', 'ConversionValue', 'Cost', 'Impressions',
                  'Interactions', 'InteractionTypes', 'VideoViews',
                  'created_at', 'updated_at')
