from django.contrib import admin

# Register your models here.
from news.models import *


class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'requests_nb', 'is_active']
    list_editable = ['is_active']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    list_editable = ['is_active']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'news_provider', 'news_category', 'news_author', 'is_top_in_category', 'is_top_news', 'is_archived']
    list_editable = ['is_top_in_category', 'is_top_news', 'is_archived']


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news', 'time', 'is_removed']
    list_editable = ['is_removed']


class ReadLaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news', 'is_removed']
    list_editable = ['is_removed']


class CMSAdmin(admin.ModelAdmin):
    list_display = ['footer_title', 'category1', 'category2', 'category3', 'category4', 'category5', 'category6']


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news', 'is_removed']
    list_editable = ['is_removed']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news', 'content', 'created_at']


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_subscribed']
    list_editable = ['is_subscribed']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    list_editable = ['is_active']


class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    list_editable = ['is_active']


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(ReadLater, ReadLaterAdmin)
admin.site.register(CMS, CMSAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(NewsSource, NewsSourceAdmin)
