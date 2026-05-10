from django.db import models
from apps.core.models import BaseModel

# Create your models here.


class ConsultationType(BaseModel):
    name = models.CharField(max_length=200, help_text="Consultation type name")
    description = models.TextField(blank=True, null=True, help_text="Consultation type description")
    fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Consultation type fee")
    is_available = models.BooleanField(default=True, help_text="Consultation type availability")
    is_recommended = models.BooleanField(default=False, help_text="Consultation type recommendation")

    facility_1 = models.CharField(max_length=200, null=True, blank=True)
    facility_2 = models.CharField(max_length=200, null=True, blank=True)
    facility_3 = models.CharField(max_length=200, null=True, blank=True)
    facility_4 = models.CharField(max_length=200, null=True, blank=True)
    facility_5 = models.CharField(max_length=200, null=True, blank=True)
    facility_6 = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Consultation Type"
        verbose_name_plural = "Consultation Types"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @classmethod
    def get_available_consultation_types(cls):
        return cls.objects.filter(is_available=True)
