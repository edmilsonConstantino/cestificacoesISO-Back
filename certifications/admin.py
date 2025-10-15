from django.contrib import admin
from django.utils.html import format_html
from .models import Certification

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "curso", "status", "ver_link")
    readonly_fields = ('unique_link', 'mostrar_link_completo')
    
    def ver_link(self, obj):
        if obj.unique_link:
            link = f"https://cptec-co-mz.vercel.app/declaracoes/{obj.unique_link}"
            return format_html(
                '<a href="{}" target="_blank" style="color: #667eea; font-weight: bold;">🔗 Ver Link</a>',
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
                '<input type="text" value="{}" readonly style="width: 100%; padding: 8px; margin-top: 5px;" onclick="this.select();">'
                '<p style="color: #666; font-size: 12px; margin-top: 5px;">Clique no campo acima para copiar o link</p>'
                '</div>',
                link
            )
        return "O Link será gerado automaticamente ao salvar"
    mostrar_link_completo.short_description = "Link para Compartilhar"
