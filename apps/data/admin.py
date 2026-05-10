from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(IntakeData)
class IntakeDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment')
    list_filter = ('appointment',)
    search_fields = ('appointment__email', 'appointment__phone')  # Search by patient
    readonly_fields = ('created_at', 'updated_at')  # Read-only fields
