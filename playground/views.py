from django.shortcuts import render
from store.models import Collection, Product


def say_hello(request):

    # collection = Collection (pk=11)
    # collection.featured_product_id = None 
    # collection.save()
    
    # collection = Collection.objects.get (pk=11)
    # collection.featured_product_id = None 
    # collection.save()
    
    # collection = Collection.objects.filter(pk=11).update(title='test collection(editted)')
    return render(request, 'hello.html', {'name': 'Mosh'})
