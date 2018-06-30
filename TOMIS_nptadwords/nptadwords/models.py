from django.db import models


class Record(models.Model):
    """
    Record Model
    Defines the attributes of an record
    """
    AccountDescriptiveName = models.CharField(max_length=255)
    CampaignId = models.IntegerField()
    CampaignName = models.CharField(max_length=255)
    CampaignStatus = models.BooleanField()
    CityCriteriaId = models.IntegerField(null=True)
    CountryCriteriaId = models.IntegerField(null=True)
    CustomerDescriptiveName = models.CharField(max_length=255)
    ExternalCustomerId = models.FloatField()
    IsTargetingLocation = models.BooleanField()
    MetroCriteriaId = models.IntegerField(null=True)
    MostSpecificCriteriaId = models.IntegerField(null=True)
    RegionCriteriaId = models.IntegerField(null=True)
    Date = models.DateField()
    Device = models.CharField(max_length=255)
    LocationType = models.CharField(max_length=255)
    AveragePosition = models.DecimalField(decimal_places=1, max_digits=5)
    Clicks = models.IntegerField()
    Conversions = models.DecimalField(decimal_places=2, max_digits=5)
    ConversionValue = models.DecimalField(decimal_places=2, max_digits=5)
    Cost = models.IntegerField()
    Impressions = models.IntegerField()
    Interactions = models.IntegerField()
    InteractionTypes = models.CharField(max_length=255)
    VideoViews = models.IntegerField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.AccountDescriptiveName + 'is added.'

    def get_CampaignName(self):
        return self.AccountDescriptiveName + ' Campaign Name is ' + self.CampaignName + '.'
