from django.urls import path
from .views import  delete_user
from django.contrib.auth.views import LoginView
from . import views
from . import utils

urlpatterns = [
    path('delete_user/', delete_user, name='delete_user'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginCheck, name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('login/', LoginView.as_view(template_name='login.html'), name='admin_login'),
    path('check_existing_id/', utils.check_existing_id, name='check_existing_id'),
    path('check_existing_email/', utils.check_existing_email, name='check_existing_email'),
    path('start_docker/', views.start_docker, name='start_docker'),
]