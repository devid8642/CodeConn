from django.contrib.auth.hashers import make_password 
from utils.tests_bases import UserTestBase
from users.models import User

class TestUserModel(UserTestBase):
    def test_user_create(self):
        user = User.objects.get(id=self.expected_user.id)
        self.assertEqual(self.expected_user, user)

    def test_user_update(self):
        self.expected_user.username = 'devid'
        self.expected_user.email = 'devid@devid.com'
        self.expected_user.password = make_password('devid3939!')
        self.expected_user.save(
            update_fields=[
                'username',
                'email',
                'password'
            ]
        )
        user = User.objects.get(id=self.expected_user.id)
        self.assertEqual(self.expected_user, user)

    def test_user_delete(self):
        self.expected_user.delete()
        exists = User.objects.filter(id=self.expected_user.id).exists()
        self.assertFalse(exists)
