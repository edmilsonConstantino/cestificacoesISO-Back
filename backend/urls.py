
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin padrão
    path('api/', include('submissions.urls')),
]