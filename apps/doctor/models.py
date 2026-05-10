from django.db import models

from apps.core.models import BaseModel
from apps.service.models import Service


# Create your models here.


class Doctor(BaseModel):
    name = models.CharField(max_length=255, help_text="Doctor name")
    services = models.ManyToManyField(Service, related_name="doctors", help_text="Services associated with this doctor")
    is_available = models.BooleanField(
        default=True,
        help_text="Doctor availability"
    )

    def __str__(self):
        return self.name