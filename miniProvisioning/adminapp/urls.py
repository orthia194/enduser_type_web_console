from django.urls import path
from . import views
from .views import home, success
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from .views import CustomLoginView, test

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('test/', views.home, name='test'),
    path('signup/', views.signup, name='signup'),
    path('success/', success, name='success'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
]