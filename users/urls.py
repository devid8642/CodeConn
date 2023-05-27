from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:id>/', views.user_detail, name='user_detail'),
    path('<int:id>/update/profile/', views.user_update, name='user_update')
]
