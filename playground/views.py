from django.shortcuts import render
from store.models import Collection, Product


def say_hello(request):

    collection = Collection()#title='test collectoin', featured_product_id=1
    collection.title = 'test collectoin'
    collection.featured_product = Product(pk=1)
    collection.featured_product_id = 1
    collection.save()
    # collection = Collection.objects.create(title='test collectoin', featured_product_id=1)
    return render(request, 'hello.html', {'name': 'Mosh'})
