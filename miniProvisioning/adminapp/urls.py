from django.urls import path
from . import views
urlpatterns = [
    path('test/', views.home, name='test'),
    path('instance_list/', views.list_ec2_instances, name='instance_list'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
]