from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Value
from store.models import Customer


def say_hello(request):

    queryset = Customer.objects.annotate(is_new=Value(True), new_id = F('id') + 1)
    return render(request, 'hello.html', {'name': 'Mosh', 'result': queryset})
