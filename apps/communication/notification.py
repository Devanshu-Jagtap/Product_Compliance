
from django.core.mail import send_mail
from django.http import HttpResponse

# def send_test_email(request):
#     subject = 'Hello from Django'
#     message = 'This is a test email sent from Django.'
#     from_email = 'jagatapdevanshu2@gmail.com'
#     recipient_list = ['pddeshmukh713@gmail.com']

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         return HttpResponse("Email sent successfully.")
#     except Exception as e:
#         return HttpResponse(f Failed to send email: {str(e)}")
    


# notifications

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_bulk_email(subject, message, recipient_list, from_email='jagatapdevanshu2@gmail.com'):
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return f"✅ Email sent to {len(recipient_list)} recipients"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"


