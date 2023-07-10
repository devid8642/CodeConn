from projects import views
from utils.tests_bases import ProjectTestBase


class NotificationsTests(ProjectTestBase):
    def test_comment_notification_view_function(self):
        self.view_test_function(
            'projects:comment_notification',
            views.comment_notification,
        )

    def test_comment_notification_showing_correctly(self):
        self.make_comment_and_login()
        response = self.response_test_function('projects:home')
        msg = 'comentou no seu post'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_empty_comment_notification(self):
        self.register_and_login()
        response = self.response_test_function('projects:home')
        msg = 'Nenhuma notificação ainda'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_comment_notification_was_viewed(self):
        self.make_comment_and_login()

        response = self.response_test_function(
            'projects:comment_notification',
            method='post',
            data={'comment_id': 1},
        )
        msg = 'Nenhuma notificação ainda'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_comment_notification_receive_get_method(self):
        self.make_comment_and_login()
        response = self.response_test_function(
            'projects:comment_notification',
        )

        self.assertEqual(response.status_code, 404)
