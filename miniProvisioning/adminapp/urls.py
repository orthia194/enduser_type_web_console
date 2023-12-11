from django.urls import path
from django.views.generic import TemplateView  # TemplateView import 추가
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    #path('instance_create/', views.instance_create, name='instance_create'),
    path('instance_create/', views.admin_ec2_view, name='instance_create'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
    path('instance_list/', views.list_ec2_instances, name='instance_list'),
    path('start_instances/', views.start_instances, name='start_instances'),
    path('stop_instances/', views.stop_instances, name='stop_instances'),
    path('terminate_instances/', views.terminate_instances, name='terminate_instances'),
    path('api_endpoint/', views.api_endpoint),#추가된코드
    path('terminal/', views.terminal),
    path('adminconsole/terminal', views.terminal, name='terminal'),
]
