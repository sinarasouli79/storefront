from django.shortcuts import render

from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('hi im sina')
    return render(request, 'playground/hello.html', {'name': 'Sina'})
