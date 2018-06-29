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