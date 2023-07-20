from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.test import override_settings
from django.core import mail

from utils.tests_bases import UserTestBase
from users.models import User
from users.tokens import account_activation_token

@override_settings(
    EMAIL_CONFIRMATION = True
)
class RegisterConfirmationTests(UserTestBase):
    def test_registered_user_confirmation_email_sended(self):
        response = self.response_test_function(
            'users:register',
            method='post',
            data=self.register_form_data
        )

        self.assertEqual(len(mail.outbox), 1)

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
