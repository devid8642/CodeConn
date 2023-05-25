from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.loginn, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutt, name='logout')
]
