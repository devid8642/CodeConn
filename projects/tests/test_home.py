from datetime import date, timedelta

from projects import views
from users.models import ProjectsDate
from utils.tests_bases import ProjectTestBase


class HomeTests(ProjectTestBase):
    def test_home_view_function(self):
        self.view_test_function('projects:home', views.home)

    def test_home_showing_approved_projects(self):
        project = self.make_project(is_approved=True)
        today = date.today()
        project_date = ProjectsDate.objects.create(
            start_date=today,
            end_date=today + timedelta(days=1),
        )
        project_date.save()

        response = self.response_test_function('projects:home')

        self.assertIn(project.title, response.content.decode('utf-8'))

    def test_home_not_showing_non_approved_projects(self):
        project = self.make_project()
        response = self.response_test_function('projects:home')

        self.assertNotIn(project.title, response.content.decode('utf-8'))

    def test_home_load_correct_template(self):
        self.template_test_function(
            'projects:home', 'projects/pages/home.html'
        )
