from django.db import models
from apps.core.models import BaseModel
from apps.doctor.models import Doctor
from apps.service.models import Service
from apps.consultation_type.models import ConsultationType


class Appointment(BaseModel):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    consultation_type = models.ForeignKey(ConsultationType, on_delete=models.CASCADE, related_name='appointments')

    first_name = models.CharField(max_length=200, help_text="Client's name")
    last_name = models.CharField(max_length=200, help_text="Client's last name")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Client's date of birth")
    state = models.CharField(max_length=100, blank=True, null=True, help_text="Client's state of residence")
    biological_sex = models.CharField(max_length=20, blank=True, null=True, help_text="Client's biological sex")
    email = models.EmailField(blank=True, null=True, help_text="Client's email address")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Client's phone number")
    
    # Medical Information
    reason_for_visit = models.TextField(blank=True, null=True, help_text="Reason for the visit")
    current_medications = models.TextField(blank=True, null=True, help_text="Current medications")
    known_allergies = models.TextField(blank=True, null=True, help_text="Known allergies")
    medical_history_info = models.TextField(blank=True, null=True, help_text="Medical history")
    
    appointment_time = models.DateTimeField(help_text="Scheduled appointment date and time")
    
    # Payment
    is_paid = models.BooleanField(default=False, help_text="Payment status")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Appointment amount")
    payment_method = models.CharField(max_length=155, help_text="Payment method")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Appointment status"
    )
    
    agreed_to_telehealth = models.BooleanField(
        default=False
    )
    agreed_to_privacy_policy = models.BooleanField(
        default=False
    )
    agreed_to_hipaa = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['-appointment_time']
        
        unique_together = ('doctor', 'appointment_time')
        indexes = [
            models.Index(fields=['-appointment_time']),
        ]

    def __str__(self):
        return f"Appointment between Dr.{self.doctor} and Patient-{self.first_name + ' ' + self.last_name} on {self.appointment_time.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        self.amount = self.consultation_type.fee
        super().save(*args, **kwargs)
    
    @classmethod
    def get_pending_appointments(cls):
        return cls.objects.filter(status='pending')

    # get all unique appointment time for a doctor 
    @classmethod
    def get_unique_appointment_times(cls, doctor_id):
        return cls.objects.filter(doctor_id=doctor_id).values_list('appointment_time', flat=True).distinct()


class AppointmentStatusHistory(BaseModel):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=250, choices=Appointment.STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f"Appointment {self.appointment.id} changed to {self.status}"