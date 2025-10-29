from rest_framework import serializers
from .models import Certification, Modulo


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id', 'nome'] 

class CertificationSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    link_completo = serializers.SerializerMethodField()

    modulos = ModuloSerializer(many=True, read_only=True)

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
            return f"https://www.cptec.co.mz/declaracoes/{obj.unique_link}"
        return None
