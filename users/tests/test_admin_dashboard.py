from datetime import date

from users import views
from users.models import ProjectsDate
from utils.tests_bases import ProjectTestBase


class AdminDashboardTests(ProjectTestBase):
    def test_admin_dashboard_view_function(self):
        self.view_test_function(
            'users:admin_dashboard',
            views.admin_dashboard,
        )

    def test_admin_dashboard_loads_correct_template(self):
        self.register_and_login(is_staff=True)

        self.template_test_function(
            'users:admin_dashboard',
            'users/pages/admin_dashboard.html',
        )

    def test_admin_dashboard_first_visit(self):
        self.register_and_login(is_staff=True)

        response = self.response_test_function('users:admin_dashboard')
        start_date = '<p><strong>Data de inicio:</strong> None</p>'
        end_date = '<p><strong>Data final:</strong> None</p>'

        self.assertIn(start_date, response.content.decode('utf-8'))
        self.assertIn(end_date, response.content.decode('utf-8'))

    def test_deadline_changed_still_on_dashboard(self):
        ProjectsDate.objects.create(
            start_date=date(2022, 6, 23), end_date=date(2030, 6, 30)
        )
        self.register_and_login(is_staff=True)
        response = self.response_test_function('users:admin_dashboard')
        start_date = '23 de Junho de 2022'
        end_date = '30 de Junho de 2030'

        self.assertIn(start_date, response.content.decode('utf-8'))
        self.assertIn(end_date, response.content.decode('utf-8'))

    def test_projects_deadline_changes(self):
        self.register_and_login(is_staff=True)

        response = self.response_test_function(
            url='users:admin_dashboard',
            method='post',
            data={
                'start_date': date(2022, 6, 23),
                'end_date': date(2022, 6, 30),
            },
        )
        start_date = '23 de Junho de 2022'
        end_date = '30 de Junho de 2022'

        self.assertIn(start_date, response.content.decode('utf-8'))
        self.assertIn(end_date, response.content.decode('utf-8'))

    def test_projects_on_deadline(self):
        ProjectsDate.objects.create(
            start_date=date(2022, 6, 23), end_date=date(2030, 6, 30)
        )
        self.register_and_login(
            email='testdate@email.com',
            is_staff=True,
        )
        self.make_project(is_approved=True)

        response = self.response_test_function('users:admin_dashboard')
        project = 'Projeto: Project title'

        self.assertIn(project, response.content.decode('utf-8'))

    def test_projects_off_deadline(self):
        ProjectsDate.objects.create(
            start_date=date(2022, 6, 23),
            end_date=date(2022, 7, 30),
        )
        self.register_and_login(
            email='testdate@email.com',
            username='datetestuser',
            is_staff=True,
        )
        self.make_project(is_approved=True)
        response = self.response_test_function('users:admin_dashboard')
        user = 'datetestuser'
        msg = 'Nenhum projeto dentro do prazo.'

        self.assertIn(user, response.content.decode('utf-8'))
        self.assertIn(msg, response.content.decode('utf-8'))
