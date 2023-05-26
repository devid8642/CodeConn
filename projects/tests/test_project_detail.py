from utils.tests_bases import ProjectTestBase
from projects import views


class ProjectDetailTests(ProjectTestBase):
    def test_project_detail_view_function(self):
        self.view_test_function(
            'projects:project_detail',
            views.project_detail,
            url_kwargs={'pk': 1},
        )

    def test_project_detail_showing_correct_project(self):
        project = self.make_project(is_approved=True)
        response = self.response_test_function(
            'projects:project_detail',
            url_kwargs={'pk': 1}
        )

        self.assertIn(project.title, response.content.decode('utf-8'))

    def test_project_detail_load_correct_template(self):
        self.make_project(is_approved=True)

        response = self.response_test_function(
            'projects:project_detail',
            url_kwargs={'pk': 1},
        )
        template = 'projects/pages/project_detail.html'

        self.assertTemplateUsed(response, template)
