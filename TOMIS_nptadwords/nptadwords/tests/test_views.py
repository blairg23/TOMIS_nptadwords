from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from ..models import Record
from ..serializers import RecordSerializers
from .. import views


class BaseViewTest(APITestCase):
    # initialize the APIClient app
    factory = APIRequestFactory()

    def setUp(self):
        # add test date
        self.test_record_1 = Record.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 1',
            CampaignId=111111111, CampaignName='Test CampaignName 1',
            CampaignStatus=True, CityCriteriaId=1111111,
            CountryCriteriaId=1111, CustomerDescriptiveName='Test CustomerDescriptiveName 1',
            ExternalCustomerId=1111111111, IsTargetingLocation=True,
            MetroCriteriaId=None, MostSpecificCriteriaId=1111111,
            RegionCriteriaId=11111, Date='2018-06-27', Device='Computers',
            LocationType='Physical Location', AveragePosition=1.3,
            Clicks=1, Conversions=0.00, ConversionValue=0.00,
            Cost=150000, Impressions=4, Interactions=1,
            InteractionTypes='[\"Clicks\"]', VideoViews=0)
        self.test_record_2 = Record.objects.create(
            AccountDescriptiveName='Test AccountDescriptiveName 2',
            CampaignId=222222222, CampaignName='Test CampaignName 2',
            CampaignStatus=False, CityCriteriaId=2222222,
            CountryCriteriaId=2222, CustomerDescriptiveName='Test CustomerDescriptiveName 2',
            ExternalCustomerId=2222222222, IsTargetingLocation=False,
            MetroCriteriaId=None, MostSpecificCriteriaId=2222222,
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
            "CampaignId": "fdsf",
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
            "Date": "2018-02-",
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
        self.RecordList = views.RecordList.as_view()
        self.RecordDetail = views.RecordDetail.as_view()


class GetAllRecordsTest(BaseViewTest):
    """ Test module for GET all record API """

    def test_get_all_records(self):
        # get API response
        request = self.factory.get('/')
        response = self.RecordList(request).render()
        # get data from db
        records = Record.objects.all()
        serializer = RecordSerializers(records, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleRecordTest(BaseViewTest):
    """  Test Module for GET single record API """

    def test_get_valid_single_record(self):
        # get API response
        request = self.factory.get('/{}'.format(self.test_record_1.pk))
        response = self.RecordDetail(request, pk=self.test_record_1.pk).render()
        # get data from db
        record = Record.objects.get(pk=self.test_record_1.pk)
        serializer = RecordSerializers(record)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_record(self):
        request = self.factory.get('/{}'.format(30))
        response = self.RecordDetail(request, pk=30).render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewRecordTest(BaseViewTest):
    """ Test module for inserting a new record """

    def test_create_valid_record(self):
        # get API response
        request = self.factory.post('/', self.valid_payload, format='json')
        response = self.RecordList(request).render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_record(self):
        # get API response
        request = self.factory.post('/', self.invalid_payload, format='json')
        response = self.RecordList(request).render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleRecordTest(BaseViewTest):
    """ Test module for updating an existing record """

    def test_valid_update_record(self):
        # get API response
        request = self.factory.put('/{}'.format(self.test_record_1.pk), self.valid_payload, format='json')
        response = self.RecordDetail(request, pk=self.test_record_1.pk).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_record(self):
        # get API response
        request = self.factory.put('/{}'.format(self.test_record_1.pk), self.invalid_payload, format='json')
        response = self.RecordDetail(request, pk=self.test_record_1.pk).render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleRecordTest(BaseViewTest):
    """ Test module for deleting an existing puppy record """

    def test_valid_delete_record(self):
        # get API response
        request = self.factory.delete('/{}'.format(self.test_record_1.pk))
        response = self.RecordDetail(request, pk=self.test_record_1.pk).render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_record(self):
        # get API response
        request = self.factory.delete('/{}'.format(40))
        response = self.RecordDetail(request, pk=40).render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
