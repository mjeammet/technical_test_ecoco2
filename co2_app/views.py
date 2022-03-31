from django.shortcuts import render
from datetime import date, datetime
from co2_app.models import Measure, InterpolateData
from django.db.models import Avg
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def index(request):

    diff_table = get_diff_table()
    graph = get_graph(diff_table)
    
    average_rates = [
        {
            "date_time": "2017-2018 weekdays",
            "real_data": round(Measure.objects.filter(date_time__iso_week_day__lte = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
            "interpolated_data": round(InterpolateData.objects.filter(date_time__iso_week_day__lte = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
        },
        {
            "date_time": "2017-2018 weekends",
            "real_data": round(Measure.objects.filter(date_time__iso_week_day__gt = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
            "interpolated_data": round(InterpolateData.objects.filter(date_time__iso_week_day__gt = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'], 2),
        }]

    context = {
        'diff_table': diff_table,
        'diff_graph': graph, 
        'average_rates': average_rates,
    }
    return render(request, 'co2_app/index.html', context)


def get_diff_table():    
    last_measurements = Measure.objects.order_by('date_time')[Measure.objects.count()-20:]
    diff_table = [{
        "date_time": measure.date_time,
        "real_data": measure.co2_rate,
        "interpolated_data": InterpolateData.objects.get(date_time=measure.date_time).co2_rate,
        "difference": int(measure.co2_rate)-int(InterpolateData.objects.get(date_time=measure.date_time).co2_rate)}
        for measure in last_measurements]    
    return diff_table


def get_graph(diff_table):
    plt.switch_backend('AGG')
    plt.figure(figsize=(15, 6))

    xcolumns = [record['date_time'] for record in diff_table]
    xcolumns_relevant = [record['date_time'] for record in diff_table if record['date_time'].minute != 0]
    yrows = [record['difference'] for record in diff_table]
    yrows_relevant = [record['difference'] for record in diff_table if record['date_time'].minute != 0]
    yrows_zero = [0]*len(yrows)

    plt.plot(xcolumns, yrows_zero, linestyle="--", color='palegreen')
    plt.plot(xcolumns, yrows, label="Including real data", linestyle=":", color='lightgray')
    plt.plot(xcolumns_relevant, yrows_relevant, label="Excluding real data")    
    plt.gcf().autofmt_xdate()
    plt.title('Difference between real and interpolated co2 rates in the last 10h of 2018.')
    plt.legend()

    # plt.table(cellText=diff_table,
    #             rowLabels=yrows,
    #                 #   rowColours=colors,
    #                   colLabels=xcolumns,
    #                   loc='bottom')
    # plt.subplots_adjust(left=0.2, bottom=0.2)


    # Writing image to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    
    return graph