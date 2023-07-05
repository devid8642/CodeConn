from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/all/', views.all_projects, name='all_projects'),
    path('project/search/', views.project_search, name='project_search'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/delete/', views.project_delete, name='project_delete'),
    path(
        'project/comment/delete', views.comment_delete, name='comment_delete'
    ),
    path(
        'project/comment/read/',
        views.comment_notification,
        name='comment_notification',
    )
]
