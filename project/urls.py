from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('mail_script.urls')),
    path('admin/', admin.site.urls),
]
