import os

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    # is_featured_category = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


class Provider(models.Model):
    host = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    requests_nb = models.IntegerField()
    dataPath_map = models.CharField(max_length=20)
    title_map = models.CharField(max_length=20)
    subTitle_map = models.CharField(max_length=20)
    content_map = models.CharField(max_length=20)
    imageUrl_map = models.CharField(max_length=20)
    provider_map = models.CharField(max_length=20)
    publishedAt_map = models.CharField(max_length=20)
    source_map = models.CharField(max_length=20)
    category_map = models.CharField(max_length=20)
    author_map = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)


#

class News(models.Model):
    title = models.CharField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateTimeField()
    url_image = models.URLField()
    news_provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    # news_source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    news_source = models.CharField(max_length=100)
    source = models.URLField()
    news_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # news_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_author = models.CharField(max_length=100)
    is_top_in_category = models.BooleanField(default=False)
    is_top_news = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)


class ReadLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    is_removed = models.BooleanField(default=False)


class CMS(models.Model):
    logo = models.URLField()
    footer_title = models.CharField(max_length=50)
    category1 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="featured_category1")
    category2 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="featured_category2")
    category3 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="featured_category3")
    category4 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="featured_category4")
    category5 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="featured_category5")
    category6 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="featured_category6")
    footer_description = models.CharField(max_length=150)
    instagram_url = models.URLField(default=None)
    facebook_url = models.URLField(default=None)
    twitter_url = models.URLField(default=None)

# class NewsSource(models.Model):
#     name = models.CharField(max_length=20, null=True)
#     is_active = models.BooleanField(default=False)
#
#
# class Subscription(models.Model):
#     email = models.EmailField()
#     is_subscribed = models.BooleanField(default=True)
#
#
# class Comment(models.Model):
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Like(models.Model):
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     is_active = models.BooleanField(default=False)
