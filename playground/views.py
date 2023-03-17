from django.shortcuts import render
from django.db.models import Count
from store.models import Customer


def say_hello(request):

    queryset = Customer.objects.annotate(orders_count=Count('order'))

    return render(request, 'hello.html', {'name': 'Mosh', 'result': queryset})
