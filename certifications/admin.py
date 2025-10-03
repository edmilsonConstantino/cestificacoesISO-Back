from django.contrib import admin
from .models import Certification

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "curso", "status")