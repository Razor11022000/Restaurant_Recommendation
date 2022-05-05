from django.http import HttpResponse
from django.shortcuts import render
from rrs.colab.ml3 import run


def index(request):
    return render(request, 'rrs/main.html')


def model(request):
    print("rss/model running.....")
    result = run('Village Whiskey', 10)
    print(result)
    context = {'result': result}
    return render(request, 'rrs/model.html', context)
