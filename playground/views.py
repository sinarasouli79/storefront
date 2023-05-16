from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import render


def say_hello(request):
    try:
        message = EmailMessage('subject', 'message', to=['test@sina.com'])
        message.attach_file('playground/static/images/iran.jpeg')
        message.send()

    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Sina'})
