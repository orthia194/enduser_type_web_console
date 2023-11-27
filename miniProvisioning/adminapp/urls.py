from django.urls import path
from . import views
from .views import home, success
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', home, name='home'),
    path('test/', views.home, name='test'),
    path('signup/', views.signup, name='signup'),
    path('success/', success, name='success'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('start_ec2_instance/', views.start_ec2_instance, name='start_ec2_instance'),
]