from django.urls import path
from django.views.generic import TemplateView  # TemplateView import 추가
from .views import  signup, success, admin_view, delete_user, CustomLoginView
from django.contrib.auth.views import LoginView
from . import views
from . import viewsec

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('instance_create/', viewsec.instance_create, name='instance_create'),
    path('start_ec2_instance/', viewsec.start_ec2_instance, name='start_ec2_instance'),
    path('instance_list/', viewsec.list_ec2_instances, name='instance_list'),
]