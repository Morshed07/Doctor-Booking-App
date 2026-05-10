from django.db import models
from apps.core.models import BaseModel
from apps.appointment.models import Appointment


class MedicalHistory(BaseModel):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='medical_history'
    )
    
    # 1. Health Goals (Multi-select checkboxes stored as a list of strings)
    health_goals = models.JSONField(
        default=list,
        blank=True,
        help_text="List of selected health goals"
    )
    
    # 2. Lifestyle Snapshot
    exercise_frequency = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    diet_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    sleep_quality = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    stress_level = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    
    # 3. Peptide / Hormone History
    used_peptides_before = models.BooleanField(
        default=False
    )
    previous_peptides_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Required if used_peptides_before is True"
    )
    peptides_used = models.JSONField(
        default=list,
        blank=True
    )
    
    # 4. Medical History & Safety (Multi-select checkboxes)
    safety_screening = models.JSONField(
        default=list,
        blank=True
    )
    relevant_medical_history = models.JSONField(
        default=list,
        blank=True
    )
    
    # 5. Treatment Goals
    treatment_goals_text = models.TextField(
        blank=True,
        null=True
    )
    desired_timeline = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    

    def __str__(self):
        return f"Medical History for {self.appointment}"
