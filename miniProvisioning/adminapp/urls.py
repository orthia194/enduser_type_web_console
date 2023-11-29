from django.urls import path
from django.views.generic import TemplateView  # TemplateView import 추가
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('instance_create/', views.instance_create, name='instance_create'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
    path('instance_list/', views.list_ec2_instances, name='instance_list'),
]