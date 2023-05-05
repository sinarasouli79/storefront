from django.shortcuts import render
from store.models import Product
from django.db import connection


def say_hello(request):

    queryset = Product.objects.raw('SELECT * FROM store_product')

    # cursor = connection.cursor()
    # queryset = cursor.execute('SELECT * FROM store_product')
    # cursor.close()

    # with connection.cursor() as cursor:
    #     # queryset =cursor.execute('SELECT * FROM store_product')
    #     queryset =cursor.callproc('get_customers', [1, 2, 'a'])
        

    return render(request, 'hello.html', {'name': 'Mosh', 'result':queryset})
