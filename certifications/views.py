from rest_framework import viewsets
from .models import Certification
from .serializers import CertificationSerializer

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer