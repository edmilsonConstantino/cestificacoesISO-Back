from rest_framework import serializers
from .models import Certification

class CertificationSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = '__all__'

    def get_foto(self, obj):
        request = self.context.get("request")
        if obj.foto:
            return request.build_absolute_uri(obj.foto.url)
        return None
