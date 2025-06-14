from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
import logging
from .models import *
from expensy.celery import app

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_otp_to_email(self, user_data):
    try:
        subject = '🔒 [Expensy] Your OTP Verification Code'
        html_message = render_to_string('send-otp.html', {
            'username': user_data['email'].split('@')[0],
            'otp': user_data['otp'],
        })
        email = EmailMessage(subject=subject,body=html_message,from_email=settings.DEFAULT_FROM_EMAIL,to=[user_data['email']],)
        email.content_subtype = 'html'
        email.send()
        return "OTP sent successfully."
    except Exception as exc:
        logger.error(f"Error sending OTP email to {user_data['email']}: {exc}")
        raise self.retry(exc=exc, countdown=10)

@app.task(bind=True)
def delete_expired_otps(self):
    expiry_time = timezone.now() - timedelta(minutes=3)
    UserOTP.objects.filter(created_at__lt=expiry_time).delete()
    print("Expired OTPsDeleted Successfully!👻")
    return {'message': 'Deleted Successfully', 'response_code': 200}
