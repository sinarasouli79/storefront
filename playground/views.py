from django.core.mail import BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        message = BaseEmailMessage(context={'name': 'sina'},
                                   template_name='playground/emails/test_email.html')
        message.send(to=['test@sina.com'])

    except BadHeaderError:
        pass
    return render(request, 'playground/hello.html', {'name': 'Sina'})
