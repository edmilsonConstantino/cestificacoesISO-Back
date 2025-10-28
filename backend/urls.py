from django.contrib import admin
from django.urls import path, include, re_path  # <- adicionar re_path
from django.conf import settings               # <- para settings.MEDIA_ROOT
from django.views.static import serve         # <- para serve
from django.http import JsonResponse

# Função de health check
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/submissions/', include('submissions.urls')),
    path('api/certifications/', include('certifications.urls')), 
    path('', health_check),  # rota raiz
]

# Servir arquivos de mídia (somente em desenvolvimento)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
