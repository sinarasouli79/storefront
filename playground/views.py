from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import OrderItem, Product


def say_hello(request):

    queryset = Product.objects.filter(id__in=OrderItem.objects.values('product').distinct()).order_by('title')
    # queryset = Product.objects.values('title').filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # queryset =OrderItem.objects.values('product__title').distinct().order_by('product__title'))
    return render(request, 'hello.html', {'name': 'Mosh', 'object_list': queryset})
