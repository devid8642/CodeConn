from utils.tests_bases import ProjectTestBase
from users import views


class AdminComplaintTests(ProjectTestBase):
    def test_project_block_view_function(self):
        self.view_test_function(
            'users:project_block',
            views.project_block,
        )

    def test_complaints_remove_view_function(self):
        self.view_test_function(
            'users:complaints_remove',
            views.complaints_remove,
        )

    def test_project_block_successfuly(self):
        project = self.make_project()
        self.register_and_login(is_staff=True)

        response = self.response_test_function(
            'users:project_block',
            method='post',
            data={'project_id': 1}
        )
        msg = f'&quot;{project.title}&quot; foi bloqueado!'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertEqual(project.is_approved, False)

    def test_project_block_receives_get_method(self):
        self.make_project()
        self.register_and_login(is_staff=True)

        response = self.response_test_function(
            'users:project_block',
            data={'project_id': 1},
        )

        self.assertEqual(response.status_code, 404)

    def test_complaints_remove_successfuly(self):
        project = self.make_project(is_approved=True)
        self.register_and_login(is_staff=True)

        response = self.response_test_function(
            'users:complaints_remove',
            method='post',
            data={'project_id': project.id},
        )
        msg = f'Denúncias de &quot;{project.title}&quot; removidas com sucesso'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_complaints_remove_receives_get_method(self):
        self.make_project()
        self.register_and_login(is_staff=True)

        response = self.response_test_function(
            'users:complaints_remove',
            data={'project_id': 1}
        )

        self.assertEqual(response.status_code, 404)
