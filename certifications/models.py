from django.db import models
import uuid

class Certification(models.Model):

    nome_completo = models.CharField(
        max_length=200,
        verbose_name="Nome Completo"
    )
    documento = models.CharField(
        max_length=50,
        verbose_name="Documento de Identificação"
    )
    foto = models.ImageField(
        upload_to='certifications/',
        blank=True,
        null=True,
        verbose_name="Foto do Estudante"
    )

    curso = models.CharField(
        max_length=200,
        verbose_name="Curso"
    )
    duracao = models.CharField(
        max_length=50,
        verbose_name="Duração do Curso"
    )
    carga_horaria = models.CharField(
        max_length=50,
        verbose_name="Carga Horária"
    )
    data_conclusao = models.DateField(
        verbose_name="Data de Conclusão"
    )
    ano = models.CharField(
        max_length=10,
        verbose_name="Ano de Conclusão"
    )
    codigo = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Código da Certificação"
    )
    status = models.CharField(
        max_length=20,
        default='Aprovado',
        verbose_name="Status"
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

    modulo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Módulo (opcional)",
        help_text="Informe o nome do módulo (ex: Módulo de Contabilidade)."
    )

    unique_link = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        editable=False,
        verbose_name="Link Único"
    )

    def save(self, *args, **kwargs):
        if not self.unique_link:
            self.unique_link = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        modulo_txt = f" - {self.modulo}" if self.modulo else ""
        return f"{self.nome_completo} - {self.curso}{modulo_txt}"

    class Meta:
        verbose_name = 'Certificação'
        verbose_name_plural = 'Certificações'
        