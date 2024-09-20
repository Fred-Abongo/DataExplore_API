from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('data_api.urls')),  
    path('', include('data_api.urls')),
]
