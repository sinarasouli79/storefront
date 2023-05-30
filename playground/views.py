import requests
from django.shortcuts import render


def say_hello(request):
    requests.get('https://httpbin.org/delay/2')
    return render(request, 'playground/hello.html', {'name': 'Sina'})
