from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import OrderItem, Product


def say_hello(request):

    queryset = Product.objects.only('title')
    return render(request, 'hello.html', {'name': 'Mosh', 'object_list': queryset})
