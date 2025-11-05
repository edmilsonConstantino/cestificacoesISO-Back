from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator

class Submission(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="Nome",
        validators=[MinLengthValidator(2, "Nome deve ter pelo menos 2 caracteres")]
    )
    email = models.EmailField(
        verbose_name="Email",
        validators=[EmailValidator(message="Email inválido")],
        db_index=True
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve estar no formato: '+258840000000'. Até 15 dígitos permitidos."
            )
        ],
        verbose_name="Telefone"
    )
    service = models.CharField(
        max_length=120,
        verbose_name="Serviço",
        db_index=True
    )
    message = models.TextField(
        verbose_name="Mensagem",
        validators=[MinLengthValidator(10, "Mensagem deve ter pelo menos 10 caracteres")]
    )
    consent = models.BooleanField(
        default=False,
        verbose_name="Consentimento"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"