from django.contrib import admin
# from unfold.admin import ModelAdmin
from .models import Doctor
# Register your models here.


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'services')
    ordering = ('-created_at',)
