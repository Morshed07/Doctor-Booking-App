from django.contrib import admin
# from unfold.admin import ModelAdmin
from .models import Service


# Register your models here.


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
