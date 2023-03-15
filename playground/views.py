from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product


def say_hello(request):
    queryset = Product.objects.filter(inventory=F('collection__id'))

    return render(request, 'hello.html', {'name': 'Mosh', 'object_list': queryset})
