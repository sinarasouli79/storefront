from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product


def say_hello(request):
    queryset = Product.objects.order_by('title')
    queryset = Product.objects.order_by('-title')
    queryset = Product.objects.filter(unit_price__gte=20).order_by('-title')
    queryset = Product.objects.filter(unit_price__gte=20).order_by('-title').reverse()
    print('earliest')
    print(Product.objects.filter(unit_price__gte=20).earliest('-title'))
    print(Product.objects.filter(unit_price__gte=20).order_by('-title')[0])

    print('latest')
    print(Product.objects.filter(unit_price__gte=20).latest('-title'))
    # print(Product.objects.filter(unit_price__gte=20).order_by('-title')[-1]) #negetive indexing is not supported.

    return render(request, 'hello.html', {'name': 'Mosh', 'object_list': queryset})
