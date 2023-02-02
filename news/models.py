import os

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    # is_featured_category = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.name}"


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

    def __str__(self) -> str:
        return self.host


class NewsSource(models.Model):
    name = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200, unique=True, db_index=True)
    subtitle = models.TextField()
    content = models.TextField()
    publish_date = models.DateTimeField()
    url_image = models.URLField()
    news_provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    news_source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    source = models.URLField()
    news_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    news_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_top_in_category = models.BooleanField(default=False)
    is_top_news = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self) -> str:
        return self.title


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, db_index=True)
    time = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Histories"


class ReadLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, db_index=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Read Later"


class CMS(models.Model):
    logo = models.ImageField(upload_to="static/svgs/")
    footer_title = models.CharField(max_length=50)
    footer_description = models.CharField(max_length=150)
    category1 = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_category1"
    )
    category2 = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_category2"
    )
    category3 = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_category3"
    )
    category4 = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_category4"
    )
    category5 = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_category5"
    )
    category6 = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_category6"
    )
    instagram_url = models.URLField(default=None)
    facebook_url = models.URLField(default=None)
    twitter_url = models.URLField(default=None)

    def save(self, *args, **kwargs):
        try:
            old_image = CMS.objects.get(pk=self.pk).logo
        except CMS.DoesNotExist:
            old_image = None
        if old_image and old_image != self.logo:
            old_image.delete(save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "CMS"

    def __str__(self) -> str:
        return f"CMS {self.id}"


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    is_removed = models.BooleanField(default=False)


class Subscription(models.Model):
    email = models.EmailField(db_index=True)
    is_subscribed = models.BooleanField(default=True)


class Tags(models.Model):
    tag = models.CharField(max_length=50, db_index=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, db_index=True)

    def __str__(self) -> str:
        return self.name
