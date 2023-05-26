from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from users.models import User


class ProjectMixin:
    def make_author(
        self,
        email: str = 'username@email.com',
        username: str = 'username',
        password: str = '123456',
    ) -> User:

        return User.objects.create(
            email=email,
            username=username,
            password=password,
        )

    def make_project(
        self,
        title: str = 'Project title',
        description: str = 'Project description',
        explanatory_text: str = 'Project explanatory',
        is_approved: bool = False,
        author_data: User = None,
    ) -> Project:

        if author_data is None:
            author_data = {}

        return Project.objects.create(
            title=title,
            description=description,
            explanatory_text=explanatory_text,
            is_approved=is_approved,
            author=self.make_author(**author_data)
        )

    def register_and_login(
        self,
        email: str = 'username@email.com',
        password: str = '123456',
    ) -> None:
        self.make_author()
        self.client.login(
            username='username',
            password='123456',
        )

    def base_test_function(
        self,
        url: str,
        url_kwargs: bool = False,
        pk: int = 1,
        method: str = 'get',
        data: dict = None,
        follow: bool = True,
    ):
        if url_kwargs:
            reversed_url = reverse(url, kwargs={'pk': pk})

        else:
            reversed_url = reverse(url)

        if method == 'get':
            response = self.client.get(
                reversed_url, data=data, follow=follow
            )

        elif method == 'post':
            response = self.client.post(
                reversed_url, data=data, follow=follow
            )

        return response


class ProjectTestBase(TestCase, ProjectMixin):
    def setUp(self, *args, **kwargs):
        '''
        Not validated yet.
        '''
        self.project_form_data = {
            **self.make_project,
        }

        self.register_form_data = {
            **self.make_author,
        }

        return super().setUp(*args, **kwargs)
