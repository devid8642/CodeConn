from utils.tests_bases import ProjectTestBase
from projects.models import Project
from projects import views


class ProjectEditTests(ProjectTestBase):
    def test_project_edit_view_function(self):
        self.view_test_function(
            'projects:project_edit',
            views.project_edit,
            {'pk': 1}
        )

    def test_project_edit_success(self):
        self.make_project_and_login()
        new_title = 'Title edited'
        self.project_form_data['title'] = new_title

        self.response_test_function(
            'projects:project_edit',
            url_kwargs={'pk': 1},
            method='post',
            data=self.project_form_data,
        )
        project = new_title

        self.assertEqual(
            Project.objects.get(id=1).title,
            project
        )

    def test_project_edit_not_found(self):
        self.register_and_login()

        response = self.response_test_function(
            'projects:project_edit',
            url_kwargs={'pk': 1},
            method='post'
        )

        self.assertEqual(response.status_code, 404)

    def test_project_edit_load_correct_template(self):
        self.make_project_and_login()

        self.template_test_function(
            'projects:project_edit',
            url_kwargs={'pk': 1},
            template_url='projects/pages/project_edit.html'
        )
