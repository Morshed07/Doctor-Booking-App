from django.db import models
from apps.core.models import BaseModel
from django.utils.safestring import mark_safe


# Create your models here.

class Product(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    def thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')
        return "No Image" 