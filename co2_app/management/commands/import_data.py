from django.core.management.base import BaseCommand

from co2_app.models import Measure

from datetime import datetime
import requests


endpoint = 'http://api-recrutement.ecoco2.com/v1/data/'
# query parameters must be decimals. See https://api-recrutement.ecoco2.com/docs/#tag/v1
start = datetime.timestamp(datetime.strptime("2017-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"))
# end = datetime.timestamp(datetime.strptime("2017-01-01T03:00:00", "%Y-%m-%dT%H:%M:%S"))
end = datetime.timestamp(datetime.strptime("2018-12-31T23:59:59", "%Y-%m-%dT%H:%M:%S"))


class Command(BaseCommand):
    help = 'Loads CO2 data from public API. Flush database'

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

        # Add collected data to local database
        added_entries = 0
        for measure in collected_data:
            measure = Measure(datetime=measure['datetime'], co2_rate=measure["co2_rate"])
            measure.save()
            added_entries += 1

        print(f"Database succesfully loaded. Added {added_entries} entries.")
