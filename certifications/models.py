from django.db import models

from django.db import models

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
    # depoimento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.curso}"

# Create your models here.
