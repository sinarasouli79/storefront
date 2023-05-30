import requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView


class HelloView(APIView):
    @method_decorator(cache_page(60 * 10))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'playground/hello.html', {'name': data})
#
# @cache_page(10 * 60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'playground/hello.html', {'name': data})
