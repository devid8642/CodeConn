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
        )  # Refactor this
        template = 'projects/pages/project_detail.html'

        self.assertTemplateUsed(response, template)

    def test_project_detail_showing_comments(self):
        comment = self.make_comment_and_login()

        response = self.response_test_function(
            'projects:project_detail',
            url_kwargs={'pk': 1},
        )

        self.assertIn(comment.comment, response.content.decode('utf-8'))

    def test_project_detail_comment_success(self):
        self.make_project_and_login()

        response = self.response_test_function(
            'projects:project_detail',
            url_kwargs={'pk': 1},
            method='post',
            data={
                'comment': 'Comment test',
            },
        )
        comment = 'Comment test'

        self.assertIn(comment, response.content.decode('utf-8'))

    def test_project_detail_comment_delete_success(self):
        comment = self.make_comment_and_login()

        response = self.response_test_function(
            'projects:comment_delete',
            method='post',
            data={'comment-id': comment.id}
        )

        self.assertEqual(response.status_code, 200)

    def test_project_detail_comment_delete_receive_get_method(self):
        comment = self.make_comment_and_login()

        response = self.response_test_function(
            'projects:comment_delete',
            data={'comment-id': comment.id}
        )

        self.assertEqual(response.status_code, 404)
