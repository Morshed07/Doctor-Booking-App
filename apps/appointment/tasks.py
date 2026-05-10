import logging
from datetime import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from apps.appointment.models import Appointment

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_appointment_confirmation_email(self, appointment_id):
    """
    Send an appointment confirmation email to the client after booking.
    """
    try:
        appointment = Appointment.objects.select_related(
            'service', 'consultation_type'
        ).get(id=appointment_id)
    except Appointment.DoesNotExist:
        logger.error(
            f"Appointment {appointment_id} not found. Cannot send confirmation email."
        )
        return

    # Build email context matching the template variables
    context = {
        'first_name': appointment.first_name,
        'date': appointment.appointment_time.strftime('%B %d, %Y'),
        'time': appointment.appointment_time.strftime('%I:%M %p'),
        'service_name': appointment.service.title if appointment.service else 'N/A',
        'consultation_type': (
            appointment.consultation_type.name
            if appointment.consultation_type
            else 'N/A'
        ),
        'fee': f"${appointment.amount:.2f}",
        'payment_link': f"{settings.FRONTEND_URL}/payment/{appointment.id}/",
        'year': datetime.now().year,
        'zelle_qr_url': 'https://backend.reactides.com/media/Zelle-QR-Code.jpeg',
    }

    try:
        # Render HTML email from template
        html_content = render_to_string(
            'appointment_email.html', context
        )
        text_content = strip_tags(html_content)

        subject = f"Appointment Confirmation - {appointment.first_name} {appointment.last_name}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [appointment.email]

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(
            f"Appointment confirmation email sent successfully for "
            f"appointment {appointment.id} to {appointment.email}"
        )

    except Exception as exc:
        logger.error(
            f"Failed to send appointment confirmation email for "
            f"appointment {appointment_id}: {exc}"
        )
        raise self.retry(exc=exc)
