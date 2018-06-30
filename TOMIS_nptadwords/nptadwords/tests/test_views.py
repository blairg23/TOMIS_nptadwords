import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Account
from ..serializers import AccountSerializers


# initialize the APIClient app
client = Client()


class GetAllAccountsTest(TestCase):
    """ Test module for GET all accounts API """

    def setUp(self):
        Account.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 1',
            CampaignId=111111111, CampaignName='Test CampaignName 1',
            CampaignStatus=True, CityCriteriaId=1111111,
            CountryCriteriaId=1111, CustomerDescriptiveName='Test CustomerDescriptiveName 1',
            ExternalCustomerId=1111111111, IsTargetingLocation=True,
            MetroCriteriaId=' --', MostSpecificCriteriaId=1111111,
            RegionCriteriaId=11111, Date='2018-06-27', Device='Computers',
            LocationType='Physical Location', AveragePosition=1.3,
            Clicks=1, Conversions=0.00, ConversionValue=0.00,
            Cost=150000, Impressions=4, Interactions=1,
            InteractionTypes='[\"Clicks\"]', VideoViews=0)
        Account.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 2',
            CampaignId=222222222, CampaignName='Test CampaignName 2',
            CampaignStatus=False, CityCriteriaId=2222222,
            CountryCriteriaId=2222, CustomerDescriptiveName='Test CustomerDescriptiveName 2',
            ExternalCustomerId=2222222222, IsTargetingLocation=False,
            MetroCriteriaId=' --', MostSpecificCriteriaId=2222222,
            RegionCriteriaId=22222, Date='2018-02-12', Device='Tablets with full browsers',
            LocationType='Location of interest', AveragePosition=1.3,
            Clicks=2, Conversions=4.00, ConversionValue=35.75,
            Cost=170000, Impressions=8, Interactions=4,
            InteractionTypes='[\"Clicks\"]', VideoViews=1)

    def test_get_all_accounts(self):
        # get API response
        response = client.get(reverse('get_post_accounts'))
        # get data from db
        accounts = Account.objects.all()
        serializer = AccountSerializers(accounts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleAccountTest(TestCase):
    """  Test Module for GET single account API """

    def setUp(self):
        self.test_account_1 = Account.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 1',
            CampaignId=111111111, CampaignName='Test CampaignName 1',
            CampaignStatus=True, CityCriteriaId=1111111,
            CountryCriteriaId=1111, CustomerDescriptiveName='Test CustomerDescriptiveName 1',
            ExternalCustomerId=1111111111, IsTargetingLocation=True,
            MetroCriteriaId=' --', MostSpecificCriteriaId=1111111,
            RegionCriteriaId=11111, Date='2018-06-27', Device='Computers',
            LocationType='Physical Location', AveragePosition=1.3,
            Clicks=1, Conversions=0.00, ConversionValue=0.00,
            Cost=150000, Impressions=4, Interactions=1,
            InteractionTypes='[\"Clicks\"]', VideoViews=0)
        self.test_account_2 = Account.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 2',
            CampaignId=222222222, CampaignName='Test CampaignName 2',
            CampaignStatus=False, CityCriteriaId=2222222,
            CountryCriteriaId=2222, CustomerDescriptiveName='Test CustomerDescriptiveName 2',
            ExternalCustomerId=2222222222, IsTargetingLocation=False,
            MetroCriteriaId=' --', MostSpecificCriteriaId=2222222,
            RegionCriteriaId=22222, Date='2018-02-12', Device='Tablets with full browsers',
            LocationType='Location of interest', AveragePosition=1.3,
            Clicks=2, Conversions=4.00, ConversionValue=35.75,
            Cost=170000, Impressions=8, Interactions=4,
            InteractionTypes='[\"Clicks\"]', VideoViews=1)

    def test_get_valid_single_account(self):
        response = client.get(
            reverse('get_delete_update_account', kwargs={'pk': self.test_account_1.pk}))
        account = Account.objects.get(pk=self.test_account_1.pk)
        serializer = AccountSerializers(account)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_account(self):
        response = client.get(
            reverse('get_delete_update_account', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewAccountTest(TestCase):
    """ Test module for inserting a new account """

    def setUp(self):
        self.valid_payload = {
            "AccountDescriptiveName": "Nashville Pedal Tavern",
            "CampaignId": "301791361",
            "CampaignName": "Nashville Pedal Tavern",
            "CampaignStatus": "enabled",
            "CityCriteriaId": "1026083",
            "CountryCriteriaId": "2840",
            "CustomerDescriptiveName": "Nashville Pedal Tavern",
            "ExternalCustomerId": "4807290630",
            "IsTargetingLocation": "true",
            "MetroCriteriaId": " --",
            "MostSpecificCriteriaId": "9013184",
            "RegionCriteriaId": "21175",
            "Date": "2018-02-11",
            "Device": "Computers",
            "LocationType": "Physical location",
            "AveragePosition": "1.3",
            "Clicks": "1",
            "Conversions": "0.00",
            "ConversionValue": "0.00",
            "Cost": "150000",
            "Impressions": "4",
            "Interactions": "1",
            "InteractionTypes": "[\"Clicks\"]",
            "VideoViews": "0"
        }
        self.invalid_payload = {
            "AccountDescriptiveName": "",
            "CampaignId": "301791361",
            "CampaignName": "Nashville Pedal Tavern",
            "CampaignStatus": "enabled",
            "CityCriteriaId": "1026083",
            "CountryCriteriaId": "2840",
            "CustomerDescriptiveName": "Nashville Pedal Tavern",
            "ExternalCustomerId": "4807290630",
            "IsTargetingLocation": "true",
            "MetroCriteriaId": " --",
            "MostSpecificCriteriaId": "9013184",
            "RegionCriteriaId": "21175",
            "Date": "2018-02-11",
            "Device": "Computers",
            "LocationType": "Physical location",
            "AveragePosition": "1.3",
            "Clicks": "1",
            "Conversions": "0.00",
            "ConversionValue": "0.00",
            "Cost": "150000",
            "Impressions": "4",
            "Interactions": "1",
            "InteractionTypes": "[\"Clicks\"]",
            "VideoViews": "0"
        }

    def test_create_valid_account(self):
        response = client.post(
            reverse('get_post_accounts'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_account(self):
        response = client.post(
            reverse('get_post_accounts'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleAccountTest(TestCase):
    """ Test module for updating an existing account record """


    def setUp(self):
        self.test_account_1 = Account.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 1',
            CampaignId=111111111, CampaignName='Test CampaignName 1',
            CampaignStatus=True, CityCriteriaId=1111111,
            CountryCriteriaId=1111, CustomerDescriptiveName='Test CustomerDescriptiveName 1',
            ExternalCustomerId=1111111111, IsTargetingLocation=True,
            MetroCriteriaId=' --', MostSpecificCriteriaId=1111111,
            RegionCriteriaId=11111, Date='2018-06-27', Device='Computers',
            LocationType='Physical Location', AveragePosition=1.3,
            Clicks=1, Conversions=0.00, ConversionValue=0.00,
            Cost=150000, Impressions=4, Interactions=1,
            InteractionTypes='[\"Clicks\"]', VideoViews=0)
        self.test_account_2 = Account.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 2',
            CampaignId=222222222, CampaignName='Test CampaignName 2',
            CampaignStatus=False, CityCriteriaId=2222222,
            CountryCriteriaId=2222, CustomerDescriptiveName='Test CustomerDescriptiveName 2',
            ExternalCustomerId=2222222222, IsTargetingLocation=False,
            MetroCriteriaId=' --', MostSpecificCriteriaId=2222222,
            RegionCriteriaId=22222, Date='2018-02-12', Device='Tablets with full browsers',
            LocationType='Location of interest', AveragePosition=1.3,
            Clicks=2, Conversions=4.00, ConversionValue=35.75,
            Cost=170000, Impressions=8, Interactions=4,
            InteractionTypes='[\"Clicks\"]', VideoViews=1)
        self.valid_payload = {
            "AccountDescriptiveName": "Nashville Pedal Tavern",
            "CampaignId": "301791361",
            "CampaignName": "Nashville Pedal Tavern",
            "CampaignStatus": "enabled",
            "CityCriteriaId": "1026083",
            "CountryCriteriaId": "2840",
            "CustomerDescriptiveName": "Nashville Pedal Tavern",
            "ExternalCustomerId": "4807290630",
            "IsTargetingLocation": "true",
            "MetroCriteriaId": " --",
            "MostSpecificCriteriaId": "9013184",
            "RegionCriteriaId": "21175",
            "Date": "2018-02-11",
            "Device": "Computers",
            "LocationType": "Physical location",
            "AveragePosition": "1.3",
            "Clicks": "1",
            "Conversions": "0.00",
            "ConversionValue": "0.00",
            "Cost": "150000",
            "Impressions": "4",
            "Interactions": "1",
            "InteractionTypes": "[\"Clicks\"]",
            "VideoViews": "0"
        }
        self.invalid_payload = {
            "AccountDescriptiveName": "",
            "CampaignId": "301791361",
            "CampaignName": "Nashville Pedal Tavern",
            "CampaignStatus": "enabled",
            "CityCriteriaId": "1026083",
            "CountryCriteriaId": "2840",
            "CustomerDescriptiveName": "Nashville Pedal Tavern",
            "ExternalCustomerId": "4807290630",
            "IsTargetingLocation": "true",
            "MetroCriteriaId": " --",
            "MostSpecificCriteriaId": "9013184",
            "RegionCriteriaId": "21175",
            "Date": "2018-02-11",
            "Device": "Computers",
            "LocationType": "Physical location",
            "AveragePosition": "1.3",
            "Clicks": "1",
            "Conversions": "0.00",
            "ConversionValue": "0.00",
            "Cost": "150000",
            "Impressions": "4",
            "Interactions": "1",
            "InteractionTypes": "[\"Clicks\"]",
            "VideoViews": "0"
        }

    def test_valid_update_account(self):
        response = client.put(
            reverse('get_delete_update_account', kwargs={'pk': self.test_account_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_account(self):
        response = client.put(
            reverse('get_delete_update_account', kwargs={'pk': self.test_account_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
