import json
import psycopg2
from datetime import datetime


def criteria_id_cleaner(id):
    try:
        return int(id)
    except(ValueError):
        return None


conn = psycopg2.connect("host=localhost dbname=nptadwords_drf user=nptadwords \
    password=nptadwords")
cur = conn.cursor()
now = datetime.now()

with open('npt_adwords_20170101_20180627.json') as f:
    data = json.load(f)
    for idx, record in enumerate(data):
        cur.execute("INSERT INTO nptadwords_record VALUES (%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (idx + 1,
                        record['AccountDescriptiveName'],
                        record['CampaignId'],
                        record['CampaignName'],
                        bool(record['CampaignStatus'] == 'enabled'),
                        criteria_id_cleaner(record['CityCriteriaId']),
                        criteria_id_cleaner(record['CountryCriteriaId']),
                        record['CustomerDescriptiveName'],
                        record['ExternalCustomerId'],
                        bool(record['IsTargetingLocation'].lower in
                             ("yes", "true", "t", "1")),
                        criteria_id_cleaner(record['MetroCriteriaId']),
                        criteria_id_cleaner(record['MostSpecificCriteriaId']),
                        criteria_id_cleaner(record['RegionCriteriaId']),
                        datetime.strptime(record['Date'], "%Y-%m-%d").date(),
                        record['Device'],
                        record['LocationType'],
                        record['AveragePosition'],
                        record['Clicks'],
                        record['Conversions'],
                        record['ConversionValue'],
                        record['Cost'],
                        record['Impressions'],
                        record['Interactions'],
                        record['InteractionTypes'],
                        record['VideoViews'],
                        now,
                        now
                     )
                    )
        conn.commit()
