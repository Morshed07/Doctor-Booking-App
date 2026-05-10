from django.contrib import admin
from .models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail', 'created_at')
    readonly_fields = ('thumbnail',)
    
admin.site.register(Product, ProductAdmin)