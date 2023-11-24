from django.urls import path
from . import views
urlpatterns = [
    path('test/', views.home, name='test'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
]