from rest_framework import serializers
from .models import Record
from datetime import datetime
from decimal import *


def criteria_id_cleaner(value):
    try:
        return int(value)
    except(ValueError):
        return None


def cast_int(key, value):
    try:
        return int(value)
    except(ValueError):
        raise serializers.ValidationError({
            key: 'This field is required to be an integer.'
        })


def cast_decimal(key, value):
    try:
        return Decimal(value)
    except(ValueError):
        raise serializers.ValidationError({
            key: 'This field is required to be an decimal.'
        })

def cast_boolean(value):
    try:
        return bool(value)
    except(ValueError):
        return bool(value.lower() == 'enabled')

def cast_datetime(key, value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except(ValueError):
        raise serializers.ValidationError({
            key: 'This field is required to be a date string in the format %Y-%m-%d .'
        })

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

    def to_internal_value(self, data):
        inc_data = {
            'AccountDescriptiveName': data.get('AccountDescriptiveName'),
            'CampaignId': data.get('CampaignId'),
            'CampaignName': data.get('CampaignName'),
            'CampaignStatus': data.get('CampaignStatus'),
            'CityCriteriaId': data.get('CityCriteriaId'),
            'CountryCriteriaId': data.get('CountryCriteriaId'),
            'CustomerDescriptiveName': data.get('CustomerDescriptiveName'),
            'ExternalCustomerId': data.get('ExternalCustomerId'),
            'IsTargetingLocation': data.get('IsTargetingLocation'),
            'MetroCriteriaId': data.get('MetroCriteriaId'),
            'MostSpecificCriteriaId': data.get('MostSpecificCriteriaId'),
            'RegionCriteriaId': data.get('RegionCriteriaId'),
            'Date': data.get('Date'),
            'Device': data.get('Device'),
            'LocationType': data.get('LocationType'),
            'AveragePosition': data.get('AveragePosition'),
            'Clicks': data.get('Clicks'),
            'Conversions': data.get('Conversions'),
            'ConversionValue': data.get('ConversionValue'),
            'Cost': data.get('Cost'),
            'Impressions': data.get('Impressions'),
            'Interactions': data.get('Interactions'),
            'InteractionTypes': data.get('InteractionTypes'),
            'VideoViews': data.get('VideoViews'),
        }

        for key, value in inc_data.items():
            print(value)
            if value is None:
                raise serializers.ValidationError({
                    key: 'This field is required.'
                })

        return {
            'AccountDescriptiveName': inc_data['AccountDescriptiveName'],
            'CampaignId': cast_int('CampaignId', inc_data['CampaignId']),
            'CampaignName': inc_data['CampaignName'],
            'CampaignStatus': cast_boolean(inc_data['CampaignStatus']),
            'CityCriteriaId': criteria_id_cleaner(inc_data['CityCriteriaId']),
            'CountryCriteriaId': criteria_id_cleaner(inc_data['CountryCriteriaId']),
            'CustomerDescriptiveName': inc_data['CustomerDescriptiveName'],
            'ExternalCustomerId': cast_int('ExternalCustomerId', inc_data['ExternalCustomerId']),
            'IsTargetingLocation': bool(inc_data['IsTargetingLocation'] in ("yes", "true", "t", "1")),
            'MetroCriteriaId': criteria_id_cleaner(inc_data['MetroCriteriaId']),
            'MostSpecificCriteriaId': criteria_id_cleaner(inc_data['MostSpecificCriteriaId']),
            'RegionCriteriaId': criteria_id_cleaner(inc_data['RegionCriteriaId']),
            'Date': cast_datetime('Date',inc_data['Date']),
            'Device': inc_data['Device'],
            'LocationType': inc_data['LocationType'],
            'AveragePosition': inc_data['AveragePosition'],
            'Clicks': cast_int('Clicks', inc_data['Clicks']),
            'Conversions': cast_decimal('Conversions', inc_data['Conversions']),
            'ConversionValue': cast_decimal('ConversionValue', inc_data['ConversionValue']),
            'Cost': cast_int('Cost', inc_data['Cost']),
            'Impressions': cast_int('Impressions', inc_data['Impressions']),
            'Interactions': cast_int('Interactions', inc_data['Interactions']),
            'InteractionTypes': inc_data['InteractionTypes'],
            'VideoViews': cast_int('VideoViews', inc_data['VideoViews']),
        }

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.AccountDescriptiveName = validated_data.get('AccountDescriptiveName', instance.AccountDescriptiveName)
        instance.CampaignId = validated_data.get('CampaignId', instance.CampaignId)
        instance.CampaignName = validated_data.get('CampaignName', instance.CampaignName)
        instance.CampaignStatus = validated_data.get('CampaignStatus', instance.CampaignStatus)
        instance.CityCriteriaId = validated_data.get('CityCriteriaId', instance.CityCriteriaId)
        instance.CountryCriteriaId = validated_data.get('CountryCriteriaId', instance.CountryCriteriaId)
        instance.CustomerDescriptiveName = validated_data.get('CustomerDescriptiveName', instance.CustomerDescriptiveName)
        instance.ExternalCustomerId = validated_data.get('ExternalCustomerId', instance.ExternalCustomerId)
        instance.IsTargetingLocation = validated_data.get('IsTargetingLocation', instance.IsTargetingLocation)
        instance.MetroCriteriaId = validated_data.get('MetroCriteriaId', instance.MetroCriteriaId)
        instance.MostSpecificCriteriaId = validated_data.get('MostSpecificCriteriaId', instance.MostSpecificCriteriaId)
        instance.RegionCriteriaId = validated_data.get('RegionCriteriaId', instance.RegionCriteriaId)
        instance.Date = validated_data.get('Date', instance.Date)
        instance.Device = validated_data.get('Device', instance.Device)
        instance.LocationType = validated_data.get('LocationType', instance.LocationType)
        instance.AveragePosition = validated_data.get('AveragePosition', instance.AveragePosition)
        instance.Clicks = validated_data.get('Clicks', instance.Clicks)
        instance.Conversions = validated_data.get('Conversions', instance.Conversions)
        instance.ConversionValue = validated_data.get('ConversionValue', instance.ConversionValue)
        instance.Cost = validated_data.get('Cost', instance.Cost)
        instance.Impressions = validated_data.get('Impressions', instance.Impressions)
        instance.Interactions = validated_data.get('Interactions', instance.Interactions)
        instance.InteractionTypes = validated_data.get('InteractionTypes', instance.AccountDescriptiveName)
        instance.VideoViews = validated_data.get('VideoViews', instance.VideoViews)
        instance.save()
        return instance
