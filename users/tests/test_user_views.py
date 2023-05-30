from utils.tests_bases import TestBase
from users.models import User
from django.urls import reverse

class TestLoginView(TestBase):
    def setUp(self, *args, **kwargs):
        self.url = 'users:login'
        return super().setUp(*args, **kwargs)

    def test_template(self):
        self.template_test_function(
            self.url,
            'auth/pages/login.html'
        )

    def test_with_valid_user(self):
        user = self.make_author()
        response = self.response_test_function(
            self.url,
            method='post',
            data={
                'email': user.email,
                'password': '123456'
            }
        )
        self.assertRedirects(
            response,
            reverse('projects:home')
        )
    
    def test_with_invalid_user(self):
        response = self.response_test_function(
            self.url,
            method='post',
            data={
                'email': 'devid@devid.com',
                'password': 'devid3939!'
            }
        )
        self.assertContains(
            response,
            text='Email ou senha inválidos'
        )


class TestRegisterView(TestBase):
    def setUp(self, *args, **kwargs):
        self.url = 'users:register'
        return super().setUp(*args, **kwargs)

    def test_template(self):
        self.template_test_function(
            self.url,
            'auth/pages/register.html'
        )

    def test_with_valid_user(self):
        data = {
            'username': 'devid',
            'email': 'devid@devid.com',
            'password': 'devid3939!',
            'confirmed_password': 'devid3939!'
        }
        response = self.response_test_function(
            self.url,
            method='post',
            data=data
        )
        self.assertRedirects(
            response,
            reverse('users:login')
        )
        self.assertTrue(
            User.objects.filter(email=data['email']).exists()
        )
    
    def test_with_invalid_user(self):
        user = self.make_author()
        response = self.response_test_function(
            self.url,
            method='post',
            data={
                'username': user.username,
                'email': user.email,
                'password': 'teste3939!',
                'confirmed_password': 'teste3939!'
            }
        )
        self.assertContains(
            response,
            'Já existe um usuário com este email'
        )
        self.assertEqual(
            len(User.objects.filter(email=user.email)),
            1
        )
