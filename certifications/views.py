from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Certification
from .serializers import CertificationSerializer

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

    @action(detail=False, methods=['get'], url_path='link/(?P<unique_link>[^/.]+)')
    def get_by_link(self, request, unique_link=None):
        try:
            certification = Certification.objects.get(unique_link=unique_link)
            serializer = self.get_serializer(certification)
            return Response(serializer.data)
        except Certification.DoesNotExist:
            return Response(
                {"error": "Certificação não encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )