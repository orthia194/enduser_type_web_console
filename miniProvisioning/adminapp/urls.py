from django.urls import path
from django.views.generic import TemplateView  # TemplateView import 추가
from .views import home, signup, success, start_ec2_instance, admin_view, delete_user, CustomLoginView, list_ec2_instances
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('test/', views.home, name='test'),
    path('instance_list/', list_ec2_instances, name='instance_list'),  # 수정
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),  # 수정
    path('login/', views.loginCheck, name='login'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),  # 수정
    path('admin_view/', views.admin_view, name='admin_view'),  # 수정
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('adminconsole/login/', LoginView.as_view(template_name='login.html'), name='admin_login'),
    path('check_existing_id/', views.check_existing_id, name='check_existing_id'),
    path('check_existing_email/', views.check_existing_email, name='check_existing_email'),
]