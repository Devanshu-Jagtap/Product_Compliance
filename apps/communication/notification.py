
from django.core.mail import send_mail
from django.http import HttpResponse
from celery import shared_task

@shared_task
def send_bulk_email(subject, message, recipient_list, from_email='jagatapdevanshu2@gmail.com'):
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return f"Email sent to {len(recipient_list)} recipients"
    except Exception as e:
        return f"Error sending email: {str(e)}"


