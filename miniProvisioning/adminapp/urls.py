from django.urls import path
from . import views
urlpatterns = [
    path('test/', views.home, name='test'),
    path('signup/', views.signup, name='signup'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
]