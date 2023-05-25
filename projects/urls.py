from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/all/', views.all_projects, name='all_projects')
]
