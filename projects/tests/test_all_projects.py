from utils.tests_bases import ProjectTestBase
from projects import views


class AllProjectsTests(ProjectTestBase):
    def test_all_projects_view(self):
        self.view_test_function(
            'projects:all_projects', views.all_projects
        )

    def test_all_projects_showing_approved_projects(self):
        project = self.make_project(is_approved=True)
        response = self.response_test_function('projects:all_projects')

        self.assertIn(project.title, response.content.decode('utf-8'))

    def test_all_projects_not_showing_non_approved_projects(self):
        project = self.make_project()
        response = self.response_test_function('projects:all_projects')

        self.assertNotIn(project.title, response.content.decode('utf-8'))

    def test_all_projects_load_correct_template(self):
        self.template_test_function(
            'projects:all_projects', 'projects/pages/all_projects.html'
        )
