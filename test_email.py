from django.core.mail import EmailMessage
from django.conf import settings

def send_test_email():
    try:
        email = EmailMessage(
            subject='Django Test Email',
            body='This is a test email sent from Django.',
            from_email=settings.EMAIL_HOST_USER,
            to=['swethaedaguttu@gmail.com'],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        result = email.send(fail_silently=False)
        print(f"Email sent successfully! Result: {result}")
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    send_test_email() 