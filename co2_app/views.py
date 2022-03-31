from django.shortcuts import render
from django.db import OperationalError
from django.db.models import Avg
from datetime import date, datetime
from io import BytesIO
import base64
import matplotlib.pyplot as plt

from co2_app.models import Measure, InterpolateData


def index(request):
    """View for index."""

    diff_table = get_diff_table(measures_to_display=20)
    
    average_rates = []
    if diff_table != None:
        average_rates = [
            {
                "period": "2017-2018 weekdays",
                "real_data": round(Measure.objects.filter(date_time__iso_week_day__lte = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
                "interpolated_data": round(InterpolateData.objects.filter(date_time__iso_week_day__lte = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
            },
            {
                "period": "2017-2018 weekends",
                "real_data": round(Measure.objects.filter(date_time__iso_week_day__gt = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
                "interpolated_data": round(InterpolateData.objects.filter(date_time__iso_week_day__gt = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
            }]        

    context = {
        'diff_table': diff_table,
        'diff_graph': get_graph(diff_table) if diff_table != None else None, 
        'average_rates': average_rates,
    }
    return render(request, 'co2_app/index.html', context)


def get_diff_table(measures_to_display=20):
    """Creates and returns a table of the last {measures_to_display} (default=20) records with datetime, real data, interpolated data and difference between the two datasets."""

    try:
        last_measurements = Measure.objects.order_by('date_time')[Measure.objects.count()-measures_to_display:]
    except OperationalError:
        print('Measure table not found. Migrate database to create sqlite3 file.')
        return None

    diff_table = [{
        "date_time": measure.date_time,
        "real_data": measure.co2_rate,
        "interpolated_data": InterpolateData.objects.get(date_time=measure.date_time).co2_rate,
        "difference": int(measure.co2_rate)-int(InterpolateData.objects.get(date_time=measure.date_time).co2_rate)}
        for measure in last_measurements]    
    return diff_table


def get_graph(diff_table):
    """Taking a diff table as input, plots and returns a graph showing difference between real and interpolated data."""
    plt.switch_backend('AGG')
    plt.figure(figsize=(20, 10))

    xcolumns = [record['date_time'] for record in diff_table]
    xcolumns_relevant = [record['date_time'] for record in diff_table if record['date_time'].minute != 0]
    yrows = [record['difference'] for record in diff_table]
    yrows_relevant = [record['difference'] for record in diff_table if record['date_time'].minute != 0]
    yrows_zero = [0]*len(yrows)

    plt.plot(xcolumns, yrows_zero, linestyle="--", color='palegreen')
    plt.plot(xcolumns, yrows, label="Including real data", linestyle=":", color='lightgray')
    plt.plot(xcolumns_relevant, yrows_relevant, label="Excluding real data")    
    plt.gcf().autofmt_xdate()
    plt.title(f'Difference between real and interpolated co2 rates in the last {len(xcolumns)} records of 2018.')
    plt.legend()

    # Add the table to the graph ? 

    # Writing image to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    
    return graph
