from django.db import models
from apps.core.models import BaseModel


# Create your models here.


class Alert(BaseModel):
    admin_email = models.EmailField(max_length=255)

    def __str__(self):
        return self.admin_email