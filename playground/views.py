from django.shortcuts import render
from django.db.models import ExpressionWrapper, F, DecimalField, Max, Count, Sum
from store.models import Customer, Collection, Product, Order


def say_hello(request):

    # 1
    queryset = Customer.objects.annotate(last_order_id=Max('order'))

    # 2
    queryset = Collection.objects.annotate(product_count=Count('product'))

    # 3
    queryset = Customer.objects.annotate(
        order_count=Count('order')).filter(order_count__gt=5)

    #4
    queryset = Customer.objects.annotate(
        total_spent=Sum(
        F('order__orderitem__quantity')* F('order__orderitem__unit_price')
        )
    )

    # 5
    queryset = Product.objects.annotate(
        total_sale=Sum(F('orderitem__quantity') * F('orderitem__unit_price'))
        # total_sale=F('orderitem__quantity') * F('orderitem__unit_price')
        ).order_by('-total_sale')[:5]

    print(queryset)
    return render(request, 'hello.html', {'name': 'Mosh', 'result': queryset})
