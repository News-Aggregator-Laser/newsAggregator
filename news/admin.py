from django.contrib import admin

# Register your models here.
from news.models import *

MAX_COUNT_PER_PAGE = 30


class ProviderAdmin(admin.ModelAdmin):
    list_display = ["id", "host", "requests_nb", "is_active"]
    list_editable = ["is_active"]
    list_search = ["id", "host"]
    list_filter = ["is_active", "requests_nb"]
    list_per_page = MAX_COUNT_PER_PAGE


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]
    list_editable = ["is_active"]
    list_search = ["id", "name"]
    list_filter = ["is_active"]
    list_per_page = MAX_COUNT_PER_PAGE


class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "news_provider",
        "news_category",
        "news_author",
        "is_top_in_category",
        "is_top_news",
        "is_archived",
    ]
    list_editable = ["is_top_in_category", "is_top_news", "is_archived"]
    list_search = ["id", "title", "news_provider", "news_category", "news_author"]
    list_filter = ["is_top_in_category", "is_top_news", "is_archived"]
    list_per_page = MAX_COUNT_PER_PAGE


class HistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "news", "time", "is_removed"]
    list_editable = ["is_removed"]
    list_search = ["id", "user", "news"]
    list_filter = ["is_removed"]
    list_per_page = MAX_COUNT_PER_PAGE


class ReadLaterAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "news", "is_removed"]
    list_editable = ["is_removed"]
    list_search = ["id", "user", "news"]
    list_filter = ["is_removed"]
    list_per_page = MAX_COUNT_PER_PAGE


class CMSAdmin(admin.ModelAdmin):
    list_display = [
        "footer_title",
        "category1",
        "category2",
        "category3",
        "category4",
        "category5",
        "category6",
    ]


class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "news", "is_removed"]
    list_editable = ["is_removed"]
    list_search = ["id", "user", "news"]
    list_filter = ["is_removed"]
    list_per_page = MAX_COUNT_PER_PAGE


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "news", "content", "created_at"]
    list_search = ["id", "user", "news", "content"]
    list_filter = ["created_at"]
    list_per_page = MAX_COUNT_PER_PAGE


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "is_subscribed"]
    list_editable = ["is_subscribed"]
    list_search = ["id", "email"]
    list_filter = ["is_subscribed"]
    list_per_page = MAX_COUNT_PER_PAGE


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]
    list_editable = ["is_active"]
    list_search = ["id", "name"]
    list_filter = ["is_active"]
    list_per_page = MAX_COUNT_PER_PAGE


class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]
    list_editable = ["is_active"]
    list_search = ["id", "name"]
    list_filter = ["is_active"]
    list_per_page = MAX_COUNT_PER_PAGE


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
