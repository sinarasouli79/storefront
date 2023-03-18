from django.shortcuts import render
from store.models import Collection, Cart, CartItem


def say_hello(request):
    # 1
    # cart = Cart.objects.create()
    # item = CartItem()
    # item.cart_id = 1
    # item.product_id = 1
    # item.quantity = 3
    # item.save()

    # 2
    # item = CartItem.objects.get(pk=1)
    # item.quantity = 6
    # item.save()

    # 3
    # Cart.objects.get(id=1).delete()
    # cart=Cart(pk=1)
    # cart.delete()
    return render(request, 'hello.html', {'name': 'Mosh'})
