from utils.tests_bases import TestBase
from ideas.models import ProjectIdea
from ideas import views


class IdeasAdminTests(TestBase):
    def test_ideas_admin_view_function(self):
        self.view_test_function(
            'ideas:ideas_admin',
            views.ideas_admin,
        )

    def test_create_idea_succesfuly(self):
        self.register_and_login(is_staff=True)

        response = self.response_test_function(
            'ideas:ideas_admin',
            method='post',
            data={
                'idea': 'Idea test',
                'stack': '1',
                'level': '1',
                'explanation': 'Idea Explanation',
            }
        )
        idea = '<h4>Idea test</h4>'

        self.assertIn(idea, response.content.decode('utf-8'))

    def test_idea_delete_succesfuly(self):
        self.register_and_login(is_staff=True)
        ProjectIdea.objects.create(
            idea='Idea test',
            stack='Backend',
            level='Fácil',
            explanation='Idea Explanation',
        )

        response = self.response_test_function(
            'ideas:idea_delete',
            method='post',
            data={'idea_id': 1}
        )
        msg = 'Ideia deletada com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_idea_delete_receive_get_method(self):
        self.register_and_login(is_staff=True)
        ProjectIdea.objects.create(
            idea='Idea test',
            stack='Backend',
            level='Fácil',
            explanation='Idea Explanation',
        )

        response = self.response_test_function(
            'ideas:idea_delete',
            data={'idea_id': 1},
        )

        self.assertEqual(response.status_code, 404)
