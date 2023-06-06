from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib import messages

from users.tokens import account_activation_token


def activate_email(request, user, to_email):
    mail_subject = 'Ative sua conta de usuário.'
    message = render_to_string(
        'auth/pages/activate-account.html',
        {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(
            request, f'Um email de confirmação foi enviado para {to_email}'
        )
    else:
        messages.error(
            request,
            f'O email de verificação não pode ser enviado para {to_email}!'
        )
