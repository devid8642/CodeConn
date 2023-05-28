from utils.tests_bases import ProjectTestBase
from projects import views
from projects.models import Project


class ProjectCreateTests(ProjectTestBase):
    def test_project_create_view_function(self):
        self.view_test_function(
            'projects:project_create',
            views.project_create,
        )

    def test_project_create_load_correct_template(self):
        self.template_test_function(
            'projects:project_create',
            'projects/pages/project_create.html',
        )

    def test_project_create_success(self):
        self.register_and_login()

        self.response_test_function(
            'projects:project_create',
            method='post',
            data=self.project_form_data
        )

        self.assertEqual(Project.objects.count(), 1)
