from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Submission
from .serializers import SubmissionSerializer

class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'message': 'Submissão recebida com sucesso!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Erro na validação dos dados.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)