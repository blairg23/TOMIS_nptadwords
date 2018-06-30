from rest_framework import serializers
from .models import Record


class RecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('AccountDescriptiveName', 'CampaignId', 'CampaignName',
                  'CampaignStatus', 'CityCriteriaId', 'CountryCriteriaId',
                  'CustomerDescriptiveName', 'ExternalCustomerId',
                  'IsTargetingLocation', 'MetroCriteriaId',
                  'MostSpecificCriteriaId', 'RegionCriteriaId', 'Date',
                  'Device', 'LocationType', 'AveragePosition', 'Clicks',
                  'Conversions', 'ConversionValue', 'Cost', 'Impressions',
                  'Interactions', 'InteractionTypes', 'VideoViews',
                  'CreatedAt', 'UpdatedAt')
