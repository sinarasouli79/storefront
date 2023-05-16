from django.core.mail import send_mail, BadHeaderError, mail_admins
from django.shortcuts import render


def say_hello(request):
    try:
        mail_admins('subject', message='admin mail', html_message='<h1>admin mail</h1>')
        send_mail(subject='test_subject', message='test message', html_message='<h1>test message</h1>',
                  from_email='info@mushbuy.com',
                  recipient_list=['sinarasouli79@gmail.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Sina'})
