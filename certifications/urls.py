from rest_framework import routers
from .views import CertificationViewSet

router = routers.DefaultRouter()
router.register(r'', CertificationViewSet)  # tudo minúsculo

urlpatterns = router.urls
