from django.urls import path
from .views import home, signup, success, start_ec2_instance, admin_view, delete_user, CustomLoginView
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('test/', views.home, name='test'),
    path('instance_list/', views.list_ec2_instances, name='instance_list'),
    path('signup/', views.signup, name='signup'),
    path('', home, name='home'),
    path('test/', home, name='test'),
    path('signup/', signup, name='signup'),
    path('success/', success, name='success'),
    path('login/', views.loginCheck, name='login'),
    path('start_ec2_instance/', start_ec2_instance, name='start_ec2_instance'),
    path('admin_view/', admin_view, name='admin_view'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('adminconsole/login/', LoginView.as_view(template_name='login.html'), name='admin_login'),
]