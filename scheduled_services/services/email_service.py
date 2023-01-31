import base64

from django.core.mail import send_mail
from django.db.models import Count, Q

from news.models import Subscription, News


def encode(code):
    return base64.b64encode(code.encode("utf-8")).decode("utf-8")


def get_most_trending_news(n):
    news = News.objects.annotate(
        likes=Count('like', filter=Q(like__is_removed=False)),
        comments=Count('comment'),
        histories=Count('history', filter=Q(history__is_removed=False))
    ).order_by('-likes', '-comments', '-histories')[:n]
    return news


class EmailService:

    def send_emails(self):
        print("Emails service is running...")
        website = "http://localhost:8000/article/"
        # loop over subscribers and send emails
        subscribers = Subscription.objects.filter(is_subscribed=True)
        news = get_most_trending_news(1)
        for subscriber in subscribers:
            unsubscribe = encode(subscriber.email)
            to_email = subscriber.email
            subject = "Laser News"
            from_email = "email@gmail.com"
            message = news.title + "\n" + news.description + "\n" + website + str(news.id)
            html_message = '<h1>' + news.title + '</h1>' + '<p>' + news.description + '</p>' + '<a href="' + website + str(
                news.id) + '">Read more</a>' + '<br><br><a href="http://localhost:8000/unsubscribe/' + unsubscribe + '">Unsubscribe</a>'
            send_mail(subject, message, from_email, [to_email], html_message=html_message)
