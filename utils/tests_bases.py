from django.test import TestCase
from django.urls import reverse, resolve

from projects.models import Project
from users.models import User


class ProjectMixin:
    def make_author(
        self,
        email: str = 'username@email.com',
        username: str = 'username',
        password: str = '123456',
    ) -> User:
        '''
        Create a user with the registration parameters.
        '''

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
        '''
        Create a project and a user to be its author.
        '''

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
        '''
        Create a user and login.
        '''
        self.make_author()
        self.client.login(
            username='username',
            password='123456',
        )

    def response_test_function(
        self,
        url: str,
        url_kwargs: bool = False,
        pk: int = 1,
        method: str = 'get',
        data: dict = None,
        follow: bool = True,
    ):
        '''
        Simplifies responses tests that use GET or POST methods.
        '''
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
        return super().setUp(*args, **kwargs)

    def view_test_function(self, url: str, view: any) -> None:
        '''
        Base view function test.
        '''
        resolved_view = resolve(reverse(url))

        self.assertIs(resolved_view.func, view)

    def template_test_function(
        self, url: str, template_url: str
    ) -> None:
        '''
        Base template test function.
        '''
        response = self.response_test_function(url)
        template = template_url

        self.assertTemplateUsed(response, template)
