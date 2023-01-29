import base64

from django.core.mail import send_mail

from news.models import Subscription


def encode(code):
    return base64.b64encode(code.encode("utf-8")).decode("utf-8")


class EmailService:

    def send_emails(self):
        print("Emails service is running...")
        # loop over subscribers and send emails
        subscribers = Subscription.objects.filter(is_subscribed=True)
        for subscriber in subscribers:
            unsubscribe = encode(subscriber.email)
            to_email = subscriber.email
            subject = "Laser News"
            from_email = "email@gmail.com"
            message = '...'
            html_message = '<p>Please click the following <a href="http://localhost:8000/verify/' \
                           '">link</a> to verify your email address.</p>'
            send_mail(subject, message, from_email, [to_email], html_message=html_message)
