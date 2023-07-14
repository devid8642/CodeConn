from utils.tests_bases import ProjectTestBase
from projects import views


class MakeComplaintTests(ProjectTestBase):
    def test_make_complaint_view_function(self):
        self.view_test_function(
            'projects:make_complaint',
            views.make_complaint,
        )

    def test_make_complaint_successfuly(self):
        project = self.make_project_and_login()
        project.author.is_staff = True

        response = self.response_test_function(
            'projects:make_complaint',
            method='post',
            data={'project_id': project.id}
        )
        msg = 'Sua denúncia foi enviada!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_make_complaint_receives_get_method(self):
        project = self.make_project_and_login()

        response = self.response_test_function(
            'projects:make_complaint',
            data={'project_id': project.id}
        )

        self.assertEqual(response.status_code, 404)
