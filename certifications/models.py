from django.db import models
from django.core.validators import MinLengthValidator
import uuid


class Certification(models.Model):
    nome_completo = models.CharField(
        max_length=200, 
        verbose_name="Nome Completo",
        validators=[MinLengthValidator(3, "Nome deve ter pelo menos 3 caracteres")]
    )
    documento = models.CharField(
        max_length=50, 
        verbose_name="Documento de Identificação",
        db_index=True
    )
    foto = models.ImageField(
        upload_to='certifications/', 
        blank=True, 
        null=True, 
        verbose_name="Foto do Estudante"
    )

    curso = models.CharField(
        max_length=200, 
        verbose_name="Curso",
        db_index=True,
        validators=[MinLengthValidator(3, "Nome do curso deve ter pelo menos 3 caracteres")]
    )
    duracao = models.CharField(max_length=50, verbose_name="Duração do Curso")
    carga_horaria = models.CharField(max_length=50, verbose_name="Carga Horária")
    data_conclusao = models.DateField(verbose_name="Data de Conclusão", db_index=True)
    ano = models.CharField(max_length=10, verbose_name="Ano de Conclusão")
    codigo = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Código da Certificação",
        db_index=True
    )
    status = models.CharField(
        max_length=20, 
        default='Aprovado', 
        verbose_name="Status",
        choices=[
            ('Aprovado', 'Aprovado'),
            ('Reprovado', 'Reprovado'),
            ('Em Andamento', 'Em Andamento'),
        ]
    )

    declaracao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Declaração",
        help_text="Texto da declaração que será exibido no Site."
    )

    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Adicione uma descrição detalhada para esta certificação."
    )

    unique_link = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        editable=False,
        verbose_name="Link Único",
        db_index=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def save(self, *args, **kwargs):
        if not self.unique_link:
            self.unique_link = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} - {self.curso}"

    class Meta:
        verbose_name = 'Certificação'
        verbose_name_plural = 'Certificações'


class Modulo(models.Model):
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name='modulos',
        verbose_name="Certificação"
    )
    nome = models.CharField(max_length=200, verbose_name="Nome do Módulo")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
