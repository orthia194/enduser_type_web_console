from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from adminapp import views as adminapp_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='login'),
    path('', TemplateView.as_view(template_name='admin_view.html'), name='admin_view'),
    path('', TemplateView.as_view(template_name='instance_list.html'), name='instance_list'),
    path('admin/', admin.site.urls),
    path('adminapp/', include('adminapp.urls')),#추가된코드
    path('adminconsole/', include('adminapp.urls')),
    path('',include('member.urls')),
    path('terminal', adminapp_views.terminal),
]
