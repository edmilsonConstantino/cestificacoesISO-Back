from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from .models import Certification, Modulo


class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    verbose_name = "Módulo"
    verbose_name_plural = "Adicionar Módulos"
    fields = ("nome",) 


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "curso", "status", "ver_link")
    readonly_fields = ('unique_link', 'mostrar_link_completo')
    list_filter = ("status",)
    search_fields = ("nome_completo", "curso", "codigo")

    fieldsets = (
        ("Dados do Estudante", {
            "fields": ("nome_completo", "documento", "foto", "declaracao", "mostrar_link_completo"),
        }),
        ("Informações do Curso", {
            "fields": ("curso", "duracao", "carga_horaria", "data_conclusao", "ano")
        }),
        ("Status e Identificação", {
            "fields": ("codigo", "status")
        }),
    )

    inlines = [ModuloInline]

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={'rows': 6, 'cols': 80, 'style': 'width: 100%;'}
            )
        },
    }

    def ver_link(self, obj):
        if obj.unique_link:
            link = f"https://cptec-co-mz.vercel.app/declaracoes/{obj.unique_link}"
            return format_html(
                '<a href="{}" target="_blank" '
                'style="color: #667eea; font-weight: bold;">🔗 Ver Link</a>',
                link
            )
        return "-"
    ver_link.short_description = "Link Único"

    def mostrar_link_completo(self, obj):
        if obj.unique_link:
            link = f"https://cptec-co-mz.vercel.app/declaracoes/{obj.unique_link}"
            return format_html(
                '<div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">'
                '<strong>Link Único:</strong><br>'
                '<input type="text" value="{}" readonly '
                'style="width: 100%; padding: 8px; margin-top: 5px;" onclick="this.select();">'
                '<p style="color: #666; font-size: 12px; margin-top: 5px;">Clique no campo acima para copiar o link</p>'
                '</div>',
                link
            )
        return "O Link será gerado automaticamente ao salvar"
    mostrar_link_completo.short_description = "Link para Compartilhar"
