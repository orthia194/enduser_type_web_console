from django.urls import path
from .views import  delete_user, reset_password, perform_password_reset
from django.contrib.auth.views import LoginView
from . import views
from . import utils
from django.contrib.auth import views as auth_views
from adminapp.views import list_ec2_instances

urlpatterns = [
    path('delete_user/', delete_user, name='delete_user'),
    path('signup/', views.signup, name='signup'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('login/', views.loginCheck, name='login'), 
    path('check_existing_id/', utils.check_existing_id, name='check_existing_id'),
    path('check_existing_email/', utils.check_existing_email, name='check_existing_email'),
    path('start_docker/', views.start_docker, name='start_docker'),
    path('reset_password', reset_password, name='reset_password'),
    path('perform_password_reset', perform_password_reset, name='perform_password_reset'),
    path('instance_list/', list_ec2_instances, name='instance_list'),
]