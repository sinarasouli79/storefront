from django.shortcuts import render
from store.models import Order, OrderItem
from django.db import transaction


# @transaction.atomic
def say_hello(request):
    with transaction.atomic:
        order = Order()
        order.customer_id = 10
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = -4
        item.unit_price = 23.00
        item.save()
    return render(request, 'hello.html', {'name': 'Mosh'})
