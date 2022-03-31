from django.core.management.base import BaseCommand

from co2_app.models import Measure, InterpolateData

from datetime import datetime
import pandas as pd
import matplotlib

datetime_format =  "%Y-%m-%dT%H:%M:%S"
start = '2017-01-01T00:00:00'
end = '2018-12-31T23:59:59'

class Command(BaseCommand):
    help = 'Clears and fills InterpolateData table from Measure table.'

    def handle(self, *args, **kwargs):
        # Clean slate
        InterpolateData.objects.all().delete()

        # Based on https://github.com/sebsanpro/test_ecoco2/blob/master/co2_rate/views.py
        # for panda data handling 
        # Cause we used R in my previous job :( 

        # Get data from Measure table and set new frequency
        measures = pd.DataFrame(
            [(data.date_time, data.co2_rate) for data in Measure.objects.all()],
            columns=['date_time', 'co2_rate'])
        measures = measures.set_index('date_time')

        other_frequency = pd.date_range(start=start, end=end, freq='1H')
        dataframe = measures[measures.index.isin(other_frequency)].reset_index()
        
        dataframe = dataframe.set_index('date_time')
    
        dataframe = dataframe.reindex(
            pd.date_range(start=start, end=end, freq='30min'))

        # Use real_data from measurement table and interpolate
        dataframe['real_data'] = measures['co2_rate']
        dataframe = dataframe.interpolate(method='linear')

        # Reset index to print datetime correctly
        dataframe.reset_index(inplace=True)
        dataframe = dataframe.rename(columns = {'index':'date_time'})
        # print(new_dataframe)

        # Fill Django table with Interpolated data
        InterpolateData.objects.bulk_create(
            [InterpolateData(date_time=dataframe.loc[j, 'date_time'], co2_rate=dataframe.loc[j, 'co2_rate']) for j in range(len(dataframe))])

        print(f"Succesfully interpolated data.")
