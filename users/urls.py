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
    path(
        'user/<int:id>/update/password/',
        views.user_update_password,
        name='user_update_password',
    ),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('admdash/', views.admin_dashboard, name='admin_dashboard'),
    path('admdash/block/', views.project_block, name='project_block'),
    path(
        'admdash/complaints/remove/',
        views.complaints_remove,
        name='complaints_remove',
    ),
]
