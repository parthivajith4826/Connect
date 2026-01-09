from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_verification_email(self, email, verification_link):
    try:
        send_mail(
            subject="Verify your email",
            message=f"Click this link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
    
@shared_task(bind=True, max_retries=3)
def send_verification_otp(self,email,otp):
    try :
        send_mail(
                subject="OTP",
                message=otp,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
        

@shared_task(bind=True, max_retries=3)
def resend_verification_otp(self,email,otp):
    try :
        send_mail(
            subject="OTP",
            message=otp,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)