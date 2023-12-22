from projects import views
from utils.tests_bases import ProjectTestBase


class ProjectDeleteTests(ProjectTestBase):
    def test_project_delete_view_function(self):
        self.view_test_function(
            'projects:project_delete', views.project_delete
        )

    def test_project_delete_success(self):
        self.make_project_and_login()

        response = self.response_test_function(
            'projects:project_delete', method='post', data={'project_id': 1}
        )

        self.assertEqual(response.status_code, 200)

    def test_project_delete_receive_get_method(self):
        self.register_and_login()
        response = self.response_test_function('projects:project_delete')

        self.assertEqual(response.status_code, 404)
