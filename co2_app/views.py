from django.shortcuts import render
from datetime import date, datetime
from co2_app.models import Measure, InterpolateData
from django.db.models import Avg
import matplotlib.pyplot as plt


def index(request):

    diff_table = get_diff_table()
    graph = get_graph(diff_table)
    average_rates = [
        {
            "date_time": "2017-2018 weekdays",
            "real_data": Measure.objects.filter(date_time__iso_week_day__lte = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'],
            "interpolated_data": InterpolateData.objects.filter(date_time__iso_week_day__lte = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'],
            #"difference": average_values[0]['real_data'] - average_values[0]['interpolated_data']
        },
        {
            "date_time": "2017-2018 weekends",
            "real_data": Measure.objects.filter(date_time__iso_week_day__gt = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'],
            "interpolated_data": InterpolateData.objects.filter(date_time__iso_week_day__gt = 5).aggregate(Avg('co2_rate'))['co2_rate__avg'],
            #"difference": average_values[0]['real_data'] - average_values[0]['interpolated_data']
        }]

    context = {
        'diff_table': diff_table,
        'graph': graph, 
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
    y = [record['difference'] for record in diff_table]
    x = [record ['date_time'] for record in diff_table]

    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    # rate_table.plt(figsize=(10,4))
    # fig = plot.get_figure()
    # fig.title('Difference between real and interpolated co2 rates in the last 10h')
    # plt.plot(x, y)
    # plt.tight_layout()

    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    plt.savefig("media/plot.png")

    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # graph = base64.b64encode(image_png)
    # graph = graph.decode('utf-8')
    # buffer.close()
    # return graph