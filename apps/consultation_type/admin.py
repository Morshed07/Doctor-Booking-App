from django.contrib import admin
from .models import ConsultationType


class ConsultationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'fee', 'is_available', 'is_recommended']
    list_filter = ['is_available', 'is_recommended']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


admin.site.register(ConsultationType, ConsultationTypeAdmin)
