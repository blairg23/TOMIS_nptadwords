from django.test import TestCase
from ..models import Record


class RecordTest(TestCase):
    ''' Test module for Record Model '''

    def setUp(self):
        Record.objects.create(
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
        Record.objects.create(
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

    def test_campaign_name(self):
        record_test_1 = Record.objects.get(
            AccountDescriptiveName='Test AccountDescriptiveName 1')
        record_test_2 = Record.objects.get(
            AccountDescriptiveName='Test AccountDescriptiveName 2')
        self.assertEqual(
            record_test_1.get_CampaignName(), "Test AccountDescriptiveName 1 Campaign Name is Test CampaignName 1.")
        self.assertEqual(
            record_test_2.get_CampaignName(), "Test AccountDescriptiveName 2 Campaign Name is Test CampaignName 2.")
