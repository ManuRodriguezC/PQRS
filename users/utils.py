from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage


def sendUserCreate(pqrs, name, num, email):
    
    # Envio al asociado
    html_message_user = render_to_string('emails/createUser.html', {
        'pqrs': pqrs,
        'name': name,
        'num': num
    })
    email_message_user = EmailMessage(
        f'PQRS Cootratiempo Creada',
        html_message_user,
        settings.EMAIL_HOST_USER,
        to=[email]
    )
    email_message_user.content_subtype = 'html'
    email_message_user.send()

def sendAsesorsCreate(num, pqrs, emails):
    # http://190.145.132.230:8001/
    URL="http://127.0.0.1:8000/pqrs/"
    
    url = f"{URL}{num}"
    html_message = render_to_string('emails/createpqrs.html', {
        'pqrs': pqrs,
        'url': url
    })
    email_message = EmailMessage(
        f"PQRS Generada - {pqrs}",
        html_message,
        settings.EMAIL_HOST_USER,
        emails,
    )
    email_message.content_subtype = 'html'
    email_message.send()
