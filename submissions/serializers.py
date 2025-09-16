from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    def validate(self, data):
        errors = {}

        if not data.get('consent'):
            errors['consent'] = "É necessário autorizar para prosseguir."

        name = data.get('name', '').strip()
        if len(name) < 2:
            errors['name'] = "Nome deve ter pelo menos 2 caracteres."
        elif len(name) > 120:
            errors['name'] = "Nome muito longo (máximo 120 caracteres)."


        message = data.get('message', '').strip()
        if len(message) < 10:
            errors['message'] = "Mensagem deve ter pelo menos 10 caracteres."
        elif len(message) > 1000:
            errors['message'] = "Mensagem muito longa (máximo 1000 caracteres)."

    #essa oarte pos para validar servico,estava dar bug
        service = data.get('service', '').strip()
        if len(service) < 2:
            errors['service'] = "Serviço deve ter pelo menos 2 caracteres."

        if errors:
            raise serializers.ValidationError(errors)

        return data