from django.contrib import admin
# from unfold.admin import ModelAdmin
from .models import Alert


# Register your models here.

class AlertAdmin(admin.ModelAdmin):
    list_display = ('admin_email', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('admin_email',)
    ordering = ('-created_at',) 


admin.site.register(Alert, AlertAdmin)