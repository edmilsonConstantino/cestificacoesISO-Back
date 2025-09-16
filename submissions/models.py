from django.db import models
from django.core.validators import RegexValidator

class Submission(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="Nome"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve estar no formato: '+258840000000'. Até 09 dígitos permitidos."
            )
        ],
        verbose_name="Telefone"
    )
    service = models.CharField(
        max_length=120,
        verbose_name="Serviço"
    )
    message = models.TextField(
        verbose_name="Mensagem"
    )
    consent = models.BooleanField(
        default=False,
        verbose_name="Consentimento"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"