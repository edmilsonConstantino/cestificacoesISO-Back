from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id', 'name', 'email', 'phone', 'service', 
            'message', 'consent', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Valida formato de email"""
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Email inválido")
        return value.strip().lower()

    def validate_name(self, value):
        """Valida nome"""
        name = value.strip()
        if len(name) < 2:
            raise serializers.ValidationError("Nome deve ter pelo menos 2 caracteres")
        if len(name) > 120:
            raise serializers.ValidationError("Nome muito longo (máximo 120 caracteres)")
        return name

    def validate_message(self, value):
        """Valida mensagem"""
        message = value.strip()
        if len(message) < 10:
            raise serializers.ValidationError("Mensagem deve ter pelo menos 10 caracteres")
        if len(message) > 1000:
            raise serializers.ValidationError("Mensagem muito longa (máximo 1000 caracteres)")
        return message

    def validate_service(self, value):
        """Valida serviço"""
        service = value.strip()
        if len(service) < 2:
            raise serializers.ValidationError("Serviço deve ter pelo menos 2 caracteres")
        return service

    def validate_phone(self, value):
        """Valida telefone"""
        phone = value.strip()
        # Remove espaços e caracteres especiais para validação
        phone_digits = ''.join(filter(str.isdigit, phone))
        if len(phone_digits) < 9:
            raise serializers.ValidationError("Número de telefone inválido")
        return phone

    def validate(self, data):
        """Validações gerais"""
        if not data.get('consent'):
            raise serializers.ValidationError({
                "consent": "É necessário autorizar para prosseguir"
            })
        return data