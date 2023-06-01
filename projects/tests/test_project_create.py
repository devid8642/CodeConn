from parameterized import parameterized

from utils.tests_bases import ProjectTestBase
from projects.forms import ProjectForm
from projects.models import Project
from projects import views


class ProjectCreateTests(ProjectTestBase):
    def test_project_create_view_function(self):
        self.view_test_function(
            'projects:project_create',
            views.project_create,
        )

    def test_project_create_load_correct_template(self):
        self.register_and_login()

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

    @parameterized.expand([
        ('title', 'Título'),
        ('subtitle', 'Subtítulo'),
        ('explanatory_text', 'Texto de explicação'),
    ])
    def test_project_create_form_labels(self, field, label):
        form = ProjectForm()
        current_label = form[field].field.label

        self.assertEqual(label, current_label)
