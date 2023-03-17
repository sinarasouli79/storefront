from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Count, Min
from store.models import Product

def say_hello(request):

    result = Product.objects.aggregate(min=Min('unit_price'), count=Count('id'))
    return render(request, 'hello.html', {'name': 'Mosh', 'result': result})
