from django.urls import path
from django.views.generic import TemplateView  # TemplateView import 추가
from .views import  signup, success, admin_view, delete_user, CustomLoginView
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('delete_user/', delete_user, name='delete_user'),
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('login/', views.loginCheck, name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('adminconsole/login/', LoginView.as_view(template_name='login.html'), name='admin_login'),
    path('check_existing_id/', views.check_existing_id, name='check_existing_id'),
    path('check_existing_email/', views.check_existing_email, name='check_existing_email'),
]