from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/all/', views.all_projects, name='all_projects'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/delete/', views.project_delete, name='project_delete'),
]
