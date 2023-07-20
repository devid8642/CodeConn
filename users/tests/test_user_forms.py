from utils.tests_bases import TestBase
from users.forms import (
    LoginForm, RegisterForm, UpdateForm,
    UpdatePasswordForm
)


class TestLoginForm(TestBase):
    def test(self):
        form = LoginForm(initial={
            'email': 'aaaaaaaaaaaaaaaaaaa',
            'password': ''
        })
        self.assertFalse(form.is_valid())


class TestRegisterForm(TestBase):
    def test_with_email_in_use(self):
        email = self.make_author().email
        form = RegisterForm(initial={
            'username': 'teste',
            'email': email,
            'password': 'teste33939!',
            'confirmed_password': 'teste33939!'
        })
        self.assertFalse(form.is_valid())
    
    def test_with_week_password(self):
        form = RegisterForm(initial={
            'username': 'teste',
            'email': 'teste@teste.com',
            'password:': 'teste123',
            'confirmed_password': 'teste123'
        })
        self.assertFalse(form.is_valid())

    def test_with_different_passwords(self):
        form = RegisterForm(initial={
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': 'teste393939!',
            'confirmed_passoword': '@teste393939!'
        })
        self.assertFalse(form.is_valid())


class TestUpdateForm(TestBase):
    def setUp(self, *args, **kwargs):
        self.user = self.make_author()
        
        return super().setUp(*args, **kwargs)
    
    def test_with_exist_email(self):
        form = UpdateForm(
            initial={
                'username': 'teste',
                'email': self.user.email
            }
        )

        self.assertFalse(form.is_valid())

    def test_validation_email(self):
        old_email = self.user.email
        form = UpdateForm(instance=self.user )
        form.instance.email = 'teste@teste.com'
        user = form.save(old_email=old_email)

        self.assertFalse(user.is_active)


class TestUpdatePasswordForm(TestBase):
    def test_with_week_password(self):
        form = UpdatePasswordForm(
            initial={
                'password': 'teste',
                'new_password': '123'
            }
        )

        self.assertFalse(form.is_valid())
