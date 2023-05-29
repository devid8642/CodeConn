from utils.tests_bases import UserTestBase
from users.forms import LoginForm, RegisterForm, UpdateForm


class TestLoginForm(UserTestBase):
    def test(self):
        form = LoginForm(initial={
            'email': 'aaaaaaaaaaaaaaaaaaa',
            'password': ''
        })
        self.assertFalse(form.is_valid())


class TestRegisterForm(UserTestBase):
    def test_with_email_in_use(self):
        form = RegisterForm(initial={
            'username': 'teste',
            'email': f'{self.expected_user.email}',
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


class TestUpdateForm(UserTestBase):
    def test_with_week_password(self):
        form = UpdateForm(initial={
            'username': 'devid',
            'email': 'devid@devid.com',
            'password': 'teste123',
            'new_password': ''
        })
        self.assertFalse(form.is_valid())
