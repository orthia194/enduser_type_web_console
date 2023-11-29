from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminconsole/', include('adminapp.urls')),
    path('',include('member.urls')),  # 이 부분이 adminapp의 URL을 포함시킵니다.
]
