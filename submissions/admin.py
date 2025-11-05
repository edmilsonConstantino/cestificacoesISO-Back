from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import csv
import datetime
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = (
        'name_with_icon', 
        'email_link', 
        'phone_formatted',
        'service_badge', 
        'created_at_formatted', 
        'consent_status',
        'actions_column'
    )
    
    list_filter = (
        ('created_at', admin.DateFieldListFilter),
        'service', 
        'consent'
    )
    
    search_fields = ('name', 'email', 'phone', 'service', 'message')
    readonly_fields = ('created_at', 'updated_at', 'submission_summary')
    ordering = ('-created_at',)
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    actions = ['export_to_csv', 'mark_as_contacted']
    
    fieldsets = (
        ('👤 Informações Pessoais', {
            'fields': ('name', 'email', 'phone'),
            'classes': ('wide',)
        }),
        ('📋 Detalhes da Solicitação', {
            'fields': ('service', 'message'),
            'classes': ('wide',)
        }),
        ('✅ Consentimento e Dados do Sistema', {
            'fields': ('consent', 'created_at', 'updated_at', 'submission_summary'),
            'classes': ('collapse',)
        }),
    )

    def name_with_icon(self, obj):
        return format_html(
            '<span style="font-weight: bold;"><i style="color: #007cba; margin-right: 5px;">👤</i>{}</span>',
            obj.name
        )
    name_with_icon.short_description = 'Nome'
    name_with_icon.admin_order_field = 'name'

    def email_link(self, obj):
        return format_html(
            '<a href="mailto:{}" style="color: #007cba; text-decoration: none;">'
            '📧 {}</a>',
            obj.email, obj.email
        )
    email_link.short_description = 'Email'
    email_link.admin_order_field = 'email'

    def phone_formatted(self, obj):
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(90deg, #e0f7fa 0%, #fffde4 100%); padding: 4px 10px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); font-family: monospace; font-size: 15px; font-weight: 500; letter-spacing: 1px;">'
                '<span style="background: #00bcd4; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 16px; margin-right: 4px;">📞</span>'
                '<span style="color: #333;">{}</span>'
                '</span>',
                obj.phone
            )
    phone_formatted.short_description = 'Telefone'
    phone_formatted.admin_order_field = 'phone'

    def service_badge(self, obj):

        color_map = {
            'ISO 14001 - Gestão Ambiental': '#28a745',
            'ISO 9001 - Gestão da Qualidade': '#007cba',
            'ISO 45001 - Saúde e Segurança': '#dc3545',
            'Higiene, Segurança e Saúde no Trabalho': '#fd7e14',
            'Monitoria, Gestão e Avaliação de Projectos': '#6f42c1',
            'NEBOSH': '#20c997'
        }
        color = color_map.get(obj.service, '#6c757d')
        
        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 7px; background: linear-gradient(90deg, {} 0%, #f8f9fa 100%); padding: 6px 14px; border-radius: 16px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); font-size: 13px; font-weight: 600; letter-spacing: 0.5px;">'
            '<span style="background: {}; color: white; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; font-size: 15px;">🏷️</span>'
            '<span style="color: #222;">{}</span>'
            '</span>',
            color, color, obj.service[:20] + ('...' if len(obj.service) > 20 else '')
        )
    service_badge.short_description = 'Serviço'
    service_badge.admin_order_field = 'service'

    def created_at_formatted(self, obj):
        now = datetime.datetime.now(obj.created_at.tzinfo)
        diff = now - obj.created_at
        
        if diff.days == 0:
            if diff.seconds < 3600:
                time_str = f"{diff.seconds // 60} min atrás"
                color = "#28a745"
            else:
                time_str = f"{diff.seconds // 3600}h atrás"
                color = "#ffc107"
        elif diff.days == 1:
            time_str = "Ontem"
            color = "#fd7e14"
        elif diff.days < 7:
            time_str = f"{diff.days} dias atrás"
            color = "#6c757d"
        else:
            time_str = obj.created_at.strftime("%d/%m/%Y")
            color = "#6c757d"
            
        return format_html(
            '<span style="color: {}; font-weight: bold;">'
            '🕒 {}</span><br>'
            '<small style="color: #6c757d;">{}</small>',
            color, time_str, obj.created_at.strftime("%H:%M")
        )
    created_at_formatted.short_description = 'Data/Hora'
    created_at_formatted.admin_order_field = 'created_at'

    def consent_status(self, obj):
        if obj.consent:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">'
                '✅ Autorizado</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">'
                '❌ Não Autorizado</span>'
            )
    consent_status.short_description = 'Consentimento'
    consent_status.admin_order_field = 'consent'

    def actions_column(self, obj):
        return format_html(
            '<a href="mailto:{}?subject=Re: {} - CPTec Academy" style="margin-right: 10px; color: #007cba;" title="Responder por email">'
            '↩️</a>'
            '<a href="tel:{}" style="color: #28a745;" title="Ligar">'
            '📞</a>',
            obj.email, obj.service, obj.phone
        )
    actions_column.short_description = 'Ações'

    def submission_summary(self, obj):
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007cba;">'
            '<h4 style="margin-top: 0; color: #007cba;">📊 Resumo da Submissão</h4>'
            '<p><strong>ID:</strong> #{}</p>'
            '<p><strong>Submissão:</strong> {}</p>'
            '<p><strong>Mensagem:</strong></p>'
            '<div style="background: white; padding: 10px; border-radius: 3px; max-height: 100px; overflow-y: auto;">{}</div>'
            '</div>',
            obj.id, obj.created_at.strftime("%d/%m/%Y às %H:%M"), 
            obj.message or "Nenhuma mensagem adicional"
        )
    submission_summary.short_description = 'Resumo Completo'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="submissions_{datetime.date.today()}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nome', 'Email', 'Telefone', 'Serviço', 'Mensagem', 'Data', 'Consentimento'])
        
        for submission in queryset:
            writer.writerow([
                submission.name,
                submission.email,
                submission.phone,
                submission.service,
                submission.message,
                submission.created_at.strftime('%d/%m/%Y %H:%M'),
                'Sim' if submission.consent else 'Não'
            ])
        
        self.message_user(request, f'{queryset.count()} submissões exportadas com sucesso!')
        return response
    
    export_to_csv.short_description = "📥 Exportar selecionadas para CSV"

    def mark_as_contacted(self, request, queryset):
        count = queryset.count()
        self.message_user(request, f'{count} submissões marcadas como contatadas!')
    
    mark_as_contacted.short_description = "✅ Marcar como constatadas"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        total_submissions = Submission.objects.count()
        today_submissions = Submission.objects.filter(
            created_at__date=datetime.date.today()
        ).count()
        
        services_stats = Submission.objects.values('service').annotate(
            count=Count('service')
        ).order_by('-count')
        
        extra_context.update({
            'total_submissions': total_submissions,
            'today_submissions': today_submissions,
            'services_stats': services_stats,
        })
        
        return super().changelist_view(request, extra_context)


# Personalizar o site admin
admin.site.site_header = 'CPTec Academy - Dashboard'
admin.site.site_title = 'CPTec Admin'
admin.site.index_title = 'Bem-vindo ao Dashboard CPTec Academy'