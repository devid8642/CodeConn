from utils.tests_bases import TestBase
from users.forms import LoginForm, RegisterForm, UpdateForm


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
    def test_with_week_password(self):
        form = UpdateForm(initial={
            'username': 'devid',
            'email': 'devid@devid.com',
        })
        self.assertFalse(form.is_valid())


class TestUpdatePasswordForm(TestBase):
    pass
