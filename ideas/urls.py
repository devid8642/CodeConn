from django.urls import path
from . import views

app_name = 'ideas'

urlpatterns = [
    path('ideas/', views.projects_ideas, name='projects_ideas'),
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('admdash/ideas/', views.ideas_admin, name='ideas_admin'),
    path('admdash/ideas/delete/', views.idea_delete, name='idea_delete'),
]
