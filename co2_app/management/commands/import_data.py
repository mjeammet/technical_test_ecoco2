from django.core.management.base import BaseCommand

from co2_app.models import Measure, InterpolateData

from datetime import datetime
import requests


endpoint = 'http://api-recrutement.ecoco2.com/v1/data/'
datetime_format =  "%Y-%m-%dT%H:%M:%S"
start = datetime.timestamp(datetime.strptime("2017-01-01T00:00:00", datetime_format))
end = datetime.timestamp(datetime.strptime("2017-01-01T20:00:00", datetime_format))
# end = datetime.timestamp(datetime.strptime("2018-12-31T23:59:59", "%Y-%m-%dT%H:%M:%S"))


class Command(BaseCommand):
    help = 'Loads CO2 data from public API and prepare secondary table for interpolation.'

    def handle(self, *args, **kwargs):

        previous_count = Measure.objects.all().count()
        if previous_count != 0:
            print(f"Database already contains {previous_count} entries! You might want to flush database beforehand.")

            print("\n\tType 'yes' to continue, or 'no' to cancel:")
            answer = input()
            if answer != "yes":
                print('Operation cancelled by user. To flush database: do `python manage.py flush`')
                exit()

        # Get data from API
        response = requests.get(f"{endpoint}?start={start}&end={end}")
        if response.status_code != 200:
            raise Exception("Could not fetch data. Check API status at http://api-recrutement.ecoco2.com/v1/data/")
        collected_data = response.json()


        # Fill real data table
        print(f"Loading {len(collected_data)} entries")
        id_offset = 0 if previous_count == 0 else previous_count+1
        Measure.objects.bulk_create(
            [Measure(id=id_offset+i, date_time=collected_data[i]['datetime'], co2_rate=collected_data[i]['co2_rate']) for i in range(len(collected_data))])
    
        print(f"Succesfully loaded {len(collected_data)} entries.")
