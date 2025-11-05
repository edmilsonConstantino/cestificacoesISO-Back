from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator

class Submission(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="Nome Completo",
        help_text="Nome completo do solicitante",
        validators=[MinLengthValidator(2, "Nome deve ter pelo menos 2 caracteres")]
    )
    email = models.EmailField(
        verbose_name="Endereço de Email",
        help_text="Email para contato e envio de informações",
        validators=[EmailValidator(message="Email inválido")],
        db_index=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Telefone de Contato",
        help_text="Formato: +258840000000 (até 15 dígitos)",
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve estar no formato: '+258840000000'. Até 15 dígitos permitidos."
            )
        ]
    )
    service = models.CharField(
        max_length=120,
        verbose_name="Serviço Solicitado",
        help_text="Tipo de curso ou serviço de interesse",
        db_index=True
    )
    message = models.TextField(
        verbose_name="Mensagem",
        help_text="Mensagem adicional ou dúvidas (mínimo 10 caracteres)",
        validators=[MinLengthValidator(10, "Mensagem deve ter pelo menos 10 caracteres")]
    )
    consent = models.BooleanField(
        default=False,
        verbose_name="Consentimento",
        help_text="Concordo em receber comunicações da CPTec Academy"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação",
        help_text="Data e hora em que a submissão foi criada",
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização",
        help_text="Data e hora da última modificação"
    )

    class Meta:
        verbose_name = "Submissão"
        verbose_name_plural = "Submissões"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"