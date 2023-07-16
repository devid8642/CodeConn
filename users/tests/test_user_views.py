from django.core import mail
from django.test import override_settings
from django.urls import reverse, resolve
from django.contrib.auth.hashers import check_password
from utils.tests_bases import TestBase
from users.models import User
from projects.models import Project


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
            reverse('projects:home')
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


class TestUserDetailView(TestBase):
    def setUp(self, *args, **kwargs):
        self.url = 'users:user_detail'
        self.user = self.make_author()

        for c in range(3):
            Project.objects.create(
                title='teste',
                subtitle='teste',
                explanatory_text='teste',
                author=self.user,
                is_approved=True
            )

        self.user_projects = Project.objects.filter(author=self.user)
        return super().setUp(*args, **kwargs)

    def test_template(self):
        self.template_test_function(
            self.url,
            url_kwargs={'id': 1},
            template_url='users/pages/user_detail.html'
        )

    def test_with_valid_owner_user(self):
        self.client.login(email=self.user.email, password='123456')
        response = self.response_test_function(
            self.url,
            url_kwargs={'id': 1}
        )
        self.assertContains(response, text=f'{self.user.username}')
        self.assertContains(response, text='Editar perfil')
        for project in self.user_projects:
            self.assertContains(response, text=f'{project.title}')

    def test_with_valid_not_owner_user(self):
        response = self.response_test_function(
            self.url,
            url_kwargs={'id': 1}
        )
        self.assertContains(response, text=f'{self.user.username}')
        self.assertNotContains(response, text='Editar perfil')
        for project in self.user_projects:
            self.assertContains(response, text=f'{project.title}')


class TestUserUpdateView(TestBase):
    def setUp(self, *args, **kwargs):
        self.url = 'users:user_update'
        self.user = self.make_author()
        self.client.login(
            email=self.user.email,
            password='123456'
        )
        return super().setUp(*args, **kwargs)

    def test_template(self):
        self.template_test_function(
            self.url,
            url_kwargs={'id': 1},
            template_url='users/pages/user_update.html'
        )

    def test_with_valid_owner_user_get(self):
        response = self.response_test_function(
            self.url,
            url_kwargs={'id': 1}
        )
        self.assertContains(response, text=f'{self.user.email}')

    def test_with_valid_owner_user_post(self):
        new_user_data = {
            'username': 'devid',
            'email': 'devid@devid.com',
        }
        response = self.response_test_function(
            self.url,
            url_kwargs={'id': 1},
            method='post',
            data=new_user_data
        )
        user = User.objects.get(id=1)
        self.assertRedirects(
            response,
            reverse('users:user_detail', kwargs={'id': 1})
        )
        self.assertEqual(user.username, new_user_data['username'])
        self.assertEqual(user.email, new_user_data['email'])

    @override_settings(
        EMAIL_CONFIRMATION = True
    )
    def test_with_valid_user_and_email_validation(self):
        new_user_data = {
            'username': 'devid',
            'email': 'devid@devid.com',
        }
        response = self.response_test_function(
            self.url,
            url_kwargs={'id': 1},
            method='post',
            data=new_user_data
        )
        user = User.objects.get(id=1)

        self.assertFalse(user.is_active)
        self.assertRedirects(
            response,
            reverse('users:login')
        )
        self.assertEqual(user.username, new_user_data['username'])
        self.assertEqual(user.email, new_user_data['email'])

    def test_with_invalid_email(self):
        User.objects.create_user(
            username='devid',
            email='devid@devid.com',
            password='devid3939!'
        )
        new_user_data = {
            'username': 'devid',
            'email': 'devid@devid.com',
        }
        response = self.response_test_function(
            self.url,
            url_kwargs={'id': 1},
            method='post',
            data=new_user_data
        )
        self.assertContains(response, text='Este email já está em uso')
        self.assertNotEqual(
            self.user.username,
            new_user_data['username']
        )
        self.assertNotEqual(
            self.user.email,
            new_user_data['email']
        )
