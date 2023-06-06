from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from utils.tests_bases import UserTestBase
from unittest import mock
import os

from users.models import User
from users.tokens import account_activation_token


class RegisterConfirmationTests(UserTestBase):
    @mock.patch.dict(os.environ, {
        "EMAIL_CONFIRMATION": "True"
    })
    def test_registered_user_confirmation_email_sended(self):
        response = self.response_test_function(
            'users:register',
            method='post',
            data=self.register_form_data
        )
        email = self.register_form_data['email']
        msg = f'Um email de confirmação foi enviado para {email}'

        self.assertIn(msg, response.content.decode('utf-8'))

    @mock.patch.dict(os.environ, {
        "EMAIL_CONFIRMATION": "True"
    })
    def test_activate_account_success(self):
        self.response_test_function(
            'users:register',
            method='post',
            data=self.register_form_data
        )
        user = User.objects.get(pk=1)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        response = self.response_test_function(
            'users:activate',
            url_kwargs={
                'uidb64': uid,
                'token': token,
            }
        )
        msg = 'Sua conta foi ativada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    @mock.patch.dict(os.environ, {
        "EMAIL_CONFIRMATION": "True"
    })
    def test_activate_account_fail(self):
        self.response_test_function(
            'users:register',
            method='post',
            data=self.register_form_data
        )
        user = User.objects.get(pk=1)
        token = account_activation_token.make_token(user)

        response = self.response_test_function(
            'users:activate',
            url_kwargs={
                'uidb64': 'changed',
                'token': token,
            }
        )
        msg = 'Não foi possível ativar sua conta!'

        self.assertIn(msg, response.content.decode('utf-8'))
