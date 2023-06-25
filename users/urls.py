from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<int:id>/', views.user_detail, name='user_detail'),
    path(
        'user/<int:id>/update/profile/', views.user_update, name='user_update'
    ),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('admdash/', views.admin_dashboard, name='admin_dashboard'),
    path('ideas/', views.projects_ideas, name='projects_ideas'),
    path('admdash/ideas/', views.ideas_admin, name='ideas_admin'),
]
