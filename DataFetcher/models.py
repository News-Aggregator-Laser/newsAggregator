from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)
    is_featured_category = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Provider(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=True)


class Author(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)


class News(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateTimeField()
    url_image = models.URLField()
    news_provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    source = models.URLField()
    news_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    news_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_top_in_category = models.BooleanField(default=False)
    is_top_news = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)


class WatchLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    is_removed = models.BooleanField(default=False)


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CMS(models.Model):
    logo = models.URLField()
    footer_title = models.CharField(max_length=50)
    footer_description = models.CharField(max_length=150)
    instagram_url = models.URLField()
    facebook_url = models.URLField()
    twitter_url = models.URLField()
