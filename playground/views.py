from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


def say_hello(request):
    queryset = Product.objects.filter(collection__id=3)
    return render(request, 'hello.html', {'name': 'Mosh', 'product_list': queryset})
