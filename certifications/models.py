from django.db import models
from django.core.validators import MinLengthValidator
import uuid


class Certification(models.Model):
    nome_completo = models.CharField(
        max_length=200, 
        verbose_name="Nome Completo do Estudante",
        help_text="Nome completo conforme documento de identificação",
        validators=[MinLengthValidator(3, "Nome deve ter pelo menos 3 caracteres")]
    )
    documento = models.CharField(
        max_length=50, 
        verbose_name="Documento de Identificação",
        help_text="BI, Passaporte ou outro documento oficial",
        db_index=True
    )
    foto = models.ImageField(
        upload_to='certifications/', 
        blank=True, 
        null=True, 
        verbose_name="Foto do Estudante",
        help_text="Foto tipo passe (opcional)"
    )

    curso = models.CharField(
        max_length=200, 
        verbose_name="Nome do Curso",
        help_text="Título completo do curso realizado",
        db_index=True,
        validators=[MinLengthValidator(3, "Nome do curso deve ter pelo menos 3 caracteres")]
    )
    duracao = models.CharField(
        max_length=50, 
        verbose_name="Duração do Curso",
        help_text="Ex: 40 horas, 3 meses, etc."
    )
    carga_horaria = models.CharField(
        max_length=50, 
        verbose_name="Carga Horária Total",
        help_text="Total de horas do curso"
    )
    data_conclusao = models.DateField(
        verbose_name="Data de Conclusão", 
        help_text="Data em que o curso foi concluído",
        db_index=True
    )
    ano = models.CharField(
        max_length=10, 
        verbose_name="Ano de Conclusão",
        help_text="Ano da certificação"
    )
    codigo = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Código da Certificação",
        help_text="Código único para validação (gerado automaticamente se vazio)",
        db_index=True
    )
    status = models.CharField(
        max_length=20, 
        default='Aprovado', 
        verbose_name="Status da Certificação",
        help_text="Status atual do estudante no curso",
        choices=[
            ('Aprovado', 'Aprovado'),
            ('Reprovado', 'Reprovado'),
            ('Em Andamento', 'Em Andamento'),
        ]
    )

    declaracao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto da Declaração",
        help_text="Texto personalizado que será exibido na declaração pública"
    )

    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição Detalhada",
        help_text="Informações adicionais sobre a certificação e conquistas"
    )

    unique_link = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        editable=False,
        verbose_name="Link Único de Compartilhamento",
        help_text="Gerado automaticamente ao salvar",
        db_index=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data de Criação",
        help_text="Data e hora de criação do registro"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Atualização",
        help_text="Data e hora da última modificação"
    )

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
        verbose_name="Certificação Relacionada",
        help_text="Certificação à qual este módulo pertence"
    )
    nome = models.CharField(
        max_length=200, 
        verbose_name="Nome do Módulo",
        help_text="Título do módulo ou unidade do curso"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Módulo do Curso"
        verbose_name_plural = "Módulos dos Cursos"
