from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Order, Customer, Collection,Product, OrderItem


def say_hello(request):

    queryset = Order.objects.order_by('-placed_at').select_related('customer').prefetch_related('orderitem_set__product')[:5]
    return render(request, 'hello.html', {'name': 'Mosh', 'orders': queryset})
