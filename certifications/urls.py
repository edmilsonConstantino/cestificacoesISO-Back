from rest_framework import routers
from django.urls import path
from .views import CertificationViewSet

router = routers.DefaultRouter()
router.register(r'', CertificationViewSet)

urlpatterns = [
    path('link/<str:unique_link>/', CertificationViewSet.as_view({'get': 'get_by_link'}), name='certification-by-link'),
] + router.urls