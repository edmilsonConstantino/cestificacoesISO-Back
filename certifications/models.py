from django.db import models
import uuid

class Certification(models.Model):
    # -------------------------
    # 🔹 Dados do Estudante
    # -------------------------
    nome_completo = models.CharField(max_length=200)
    documento = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='certifications/', blank=True, null=True)

    # -------------------------
    # 🔹 Dados do Curso
    # -------------------------
    curso = models.CharField(max_length=200)
    duracao = models.CharField(max_length=50)
    carga_horaria = models.CharField(max_length=50)
    data_conclusao = models.DateField()
    ano = models.CharField(max_length=10)
    codigo = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='Aprovado')

    # -------------------------
    # 🧾 Conteúdo do Certificado
    # -------------------------
    declaracao = models.TextField(
        blank=True,
        null=True,
        help_text="Texto da declaração que será exibido no certificado."
    )

    # -------------------------
    # 📝 Campo de Descrição
    # -------------------------
    descricao = models.TextField(
        blank=True,
        null=True,
        help_text="Adicione uma descrição detalhada para esta certificação."
    )

    # -------------------------
    # 🔹 Módulos (opcional)
    # -------------------------
    modulo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Módulo (opcional)",
        help_text="Informe o nome do módulo (ex: Módulo de Contabilidade)."
    )
    tem_modulos = models.BooleanField(default=False, editable=False)

    # -------------------------
    # 🔗 Campos automáticos
    # -------------------------
    unique_link = models.CharField(max_length=100, unique=True, blank=True, null=True, editable=False)

    # -------------------------
    # ⚙️ Métodos
    # -------------------------
    def save(self, *args, **kwargs):
        # Gera link único se não existir
        if not self.unique_link:
            self.unique_link = str(uuid.uuid4())
        super().save(*args, **kwargs)

        # Atualiza o status do campo tem_modulos se houver relacionamento com Modulo
        if hasattr(self, 'modulos'):
            has_modulos = self.modulos.exists()
            if self.tem_modulos != has_modulos:
                self.tem_modulos = has_modulos
                super().save(update_fields=['tem_modulos'])

    def __str__(self):
        modulo_txt = f" - {self.modulo}" if self.modulo else ""
        return f"{self.nome_completo} - {self.curso}{modulo_txt}"

    class Meta:
        verbose_name = 'Certificação'
        verbose_name_plural = 'Certificações'


class Modulo(models.Model):
    certification = models.ForeignKey(
        Certification,
        related_name='modulos',
        on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
