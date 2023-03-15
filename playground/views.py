from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from store.models import Product


def say_hello(request):
    queryset = Product.objects.filter(collection__id=3)
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))
    # queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    return render(request, 'hello.html', {'name': 'Mosh', 'object_list': queryset})
