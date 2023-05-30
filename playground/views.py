import requests
from django.core.cache import cache
from django.shortcuts import render


def say_hello(request):
    key = 'httpbin'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)
    return render(request, 'playground/hello.html', {'name': cache.get(key)})
