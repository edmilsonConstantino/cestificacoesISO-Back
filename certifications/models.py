from django.db import models
import uuid

class Certification(models.Model):
    nome_completo = models.CharField(max_length=200)
    documento = models.CharField(max_length=50)
    curso = models.CharField(max_length=200)
    duracao = models.CharField(max_length=50)
    carga_horaria = models.CharField(max_length=50)
    data_conclusao = models.DateField()
    codigo = models.CharField(max_length=100, unique=True)
    ano = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='Aprovado')
    foto = models.ImageField(upload_to='certifications/', blank=True, null=True)
    unique_link = models.CharField(max_length=100, unique=True, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.unique_link:
            self.unique_link = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} - {self.curso}"

    class Meta:
        verbose_name = 'Certificação'
        verbose_name_plural = 'Certificações'
        