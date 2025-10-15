from rest_framework import serializers
from .models import Certification

class CertificationSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    link_completo = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = '__all__'

    def get_foto(self, obj):
        request = self.context.get("request")
        if obj.foto and request:
            return request.build_absolute_uri(obj.foto.url)
        elif obj.foto:
            return obj.foto.url
        return None
    
    def get_link_completo(self, obj):
        if obj.unique_link:
            # ALTERE para o domínio do seu frontend
            return f"http://localhost:8080/declaracoes/{obj.unique_link}"
        return None