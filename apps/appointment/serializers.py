from rest_framework import serializers
from .models import Appointment, AppointmentStatusHistory
from apps.history.models import MedicalHistory
from apps.history.serializers import MedicalHistorySerializer
from apps.service.models import Service
from .tasks import send_appointment_confirmation_email
from apps.notification.tasks import send_admin_appointment_notification_email


class AppointmentSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    # Nested Serializer for the survey
    medical_history = MedicalHistorySerializer(source='medicalhistory', required=False)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'service', 'consultation_type', 'appointment_time',
            'first_name', 'last_name', 'email', 'phone', 'reason_for_visit',
            'current_medications', 'known_allergies', 'medical_history_info',
            'date_of_birth', 'state', 'biological_sex', 'payment_method',
            'amount', 'status', 'is_paid', 'created_at', 'updated_at',
            'agreed_to_telehealth', 'agreed_to_privacy_policy', 'agreed_to_hipaa',
            'medical_history' # Related MedicalHistory object via reverse relationship
        ]
        read_only_fields = ['status', 'is_paid', 'amount', 'created_at', 'updated_at']

    def get_amount(self, obj):
        return obj.consultation_type.fee

    def validate(self, data):
        service = data.get('service')

        if service and not Service.objects.filter(pk=service.pk).exists():
            raise serializers.ValidationError({
                "service": "The selected service is not valid."
            })
        if not data.get('agreed_to_telehealth'):
            raise serializers.ValidationError("You must agree to all consents.")

        # 2. Check the conditional peptide logic
        used_peptides = data.get('used_peptides_before')
        peptide_details = data.get('previous_peptides_details')

        if used_peptides and not peptide_details:
            # If they checked 'Yes' but left the text box empty
            raise serializers.ValidationError({
                "previous_peptides_details": "Please specify which peptides you have used before."
            })
        
        # 3. Clean up: If they checked 'No', ensure the text field is wiped 
        # (in case they typed something, then changed their mind and clicked 'No')
        if not used_peptides:
            data['previous_peptides_details'] = ""

        return data

    def create(self, validated_data):
        # Extract fields that are not model fields
        medical_history_data = validated_data.pop('medicalhistory', None)
        validated_data.pop('previous_peptides_details', None)
        
        # Create appointment
        appointment = Appointment.objects.create(**validated_data)
        
        # Create medical history linked to the new appointment
        if medical_history_data:
            MedicalHistory.objects.create(appointment=appointment, **medical_history_data)
        
        # Send confirmation email to patient
        if appointment.email:
            send_appointment_confirmation_email.delay(appointment.id)
        
        # Send admin notification email
        send_admin_appointment_notification_email.delay(appointment.id)
        
        return appointment
       

class AppointmentStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatusHistory
        fields = [
            'id',
            'appointment',
            'status',
            'created_at',
        ]