import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from apps.appointment.models import Appointment
from apps.notification.models import Alert

logger = logging.getLogger(__name__)


def send_admin_appointment_notification_email(appointment_id):
    try:
        alert_emails = list(Alert.objects.values_list('admin_email', flat=True))
        if not alert_emails:
            logger.warning("No admin alert emails configured. Skipping admin notification.")
            return
        appointment = Appointment.objects.select_related(
            'service', 'consultation_type'
        ).get(id=appointment_id)

        context = {
        'appointment_id': appointment.id,
        'first_name': appointment.first_name,
        'last_name': appointment.last_name,
        'patient_email': appointment.email or 'N/A',
        'patient_phone': appointment.phone or 'N/A',
        'dob': appointment.date_of_birth.strftime('%B %d, %Y') if appointment.date_of_birth else 'N/A',
        'date': appointment.appointment_time.strftime('%B %d, %Y'),
        'time': appointment.appointment_time.strftime('%I:%M %p'),
        'service_name': appointment.service.title if appointment.service else 'N/A',
        'consultation_type': (
            appointment.consultation_type.name
            if appointment.consultation_type
            else 'N/A'
        ),
        'provider_name': appointment.doctor.user.get_full_name() if appointment.doctor else 'N/A',
        'booking_source': 'Online',
        'fee': f"${appointment.amount}" if appointment.amount else 'N/A',
        'payment_method': appointment.payment_method or 'N/A',
        'transaction_ref': 'Pending',
        'created_at': appointment.created_at.strftime('%B %d, %Y %I:%M %p') if hasattr(appointment, 'created_at') else 'N/A',
        'email_sent_at': 'N/A',
        }
        # Render HTML email
        html_content = render_to_string(
            'notification/admin_alert.html',
            context=context
        )
        text_content = strip_tags(html_content)

        subject = f"New Appointment Notification"
        from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=alert_emails,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(
            f"Admin appointment notification email sent successfully "
            f"to {alert_emails}"
        )

    except Exception as exc:
        logger.error(
            f"Failed to send admin notification email: {exc}",
            exc_info=True
        )