from .models import Measure, InterpolateData
from django.shortcuts import render


def index(request):

    last_measurements = Measure.objects.order_by('-datetime')[:20]
    last_interpolations = InterpolateData.objects.order_by('-datetime')[:20]

    # week = new_dataframe[new_dataframe.index.dayofweek < 5]  # filter DataFrame into working days
    # weekends = new_dataframe[new_dataframe.index.dayofweek > 4]  # filter DataFrame into weekends
    # df = new_dataframe[-20:]
    # plot = df.plot(figsize=(10, 10))
    # fig = plot.get_figure()
    # fig.savefig("media/plot.png")
    # new_dataframe.loc['mean working day'] = week.mean()
    # new_dataframe.loc['mean weekends'] = weekends.mean()


    context = {
        'last_measurements': last_measure,
        'last_interpolations': last_interpolations,
    }
    return render(request, 'co2_app/index.html', context)
