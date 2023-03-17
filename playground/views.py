from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Count, Sum, Min, Max, Avg
from django.db.models import F
from store.models import Order, OrderItem, Product


def say_hello(request):

    # 1
    result = Order.objects.aggregate(count=Count(id))

    # 2
    result = OrderItem.objects.filter(
        product__id=1).aggregate(units_sold=Sum('quantity'))
    # print(result)
    result = Product.objects.filter(id=1).aggregate(
        units_sold=Sum('orderitem__quantity'))

    # 3
    result = Order.objects.filter(customer__id=1).aggregate(Count('id'))

    # 4
    result = Product.objects \
        .filter(collection__id=3) \
        .aggregate(
            min_price=Min('unit_price'),
            max_price=Max('unit_price'),
            avg_price=Avg('unit_price')
        )
    return render(request, 'hello.html', {'name': 'Mosh', 'result': result})
