from django.shortcuts import render

import requests

def index(request):

    req = requests.get('http://api-recrutement.ecoco2.com/v1/data/')
    print(req)


    context = {}
    return render(request, 'co2_app/index.html', context)
