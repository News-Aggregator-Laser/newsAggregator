from datetime import timedelta

from django.utils import timezone

from news.models import News


class DbCleaner:
    def clean_db(self):
        print("Db cleaner is running...")
        # Archive all news records that are older than 30 days
        News.objects.filter(created_at__lte=timezone.now() - timedelta(days=30)).update(is_archived=True)
        # Delete all archived news records that are older than 60 days
        News.objects.filter(created_at__lte=timezone.now() - timedelta(days=60), is_archived=True).delete()
