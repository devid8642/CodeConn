from utils.tests_bases import ProjectTestBase
from projects import views


class HomeTests(ProjectTestBase):
    def test_home_view_function(self):
        self.view_test_function('projects:home', views.home)

    def test_home_showing_approved_projects(self):
        self.make_project(is_approved=True)

        response = self.response_test_function('projects:home')
        project = 'Project title'

        self.assertIn(project, response.content.decode('utf-8'))

    def test_home_not_showing_non_approved_projects(self):
        self.make_project()

        response = self.response_test_function('projects:home')
        project = 'Project title'

        self.assertNotIn(project, response.content.decode('utf-8'))

    def test_home_loads_correct_template(self):
        self.template_test_function(
            'projects:home', 'projects/pages/home.html'
        )
