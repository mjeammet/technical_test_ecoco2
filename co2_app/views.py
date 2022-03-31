from .models import Measure
from django.shortcuts import render


def index(request):

    last_measure = Measure.objects.order_by('-datetime')[:20]

    context = {
        'last_measurements': last_measure,
    }
    return render(request, 'co2_app/index.html', context)
