from utils.tests_bases import ProjectTestBase
from projects import views

from django.urls import reverse


class ProjectSearchTests(ProjectTestBase):
    def test_project_search_view_function(self):
        self.view_test_function(
            'projects:project_search',
            views.project_search,
        )

    def test_project_search_success(self):
        project = self.make_project(is_approved=True)
        search_term = 'title'

        search_url = reverse('projects:project_search')
        response = self.client.get(
            f'{search_url}?q={search_term}'
        )

        self.assertIn(project.title, response.content.decode('utf-8'))

    def test_project_search_raises_404_if_no_search_term(self):
        search_term = ''

        search_url = reverse('projects:project_search')
        response = self.client.get(
            f'{search_url}?q={search_term}'
        )

        self.assertEqual(response.status_code, 404)

    def test_project_search_load_correct_template(self):
        self.make_project(is_approved=True)
        search_term = 'title'

        search_url = reverse('projects:project_search')
        response = self.client.get(
            f'{search_url}?q={search_term}'
        )

        self.assertTemplateUsed(
            response,
            'projects/pages/project_search.html'
        )
