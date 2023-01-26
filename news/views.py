from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import *


def authenticated_required(function=None, redirect_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Create your views here.
def _common_vars(is_anonymous) -> dict:
    return {
        "is_authenticated": not is_anonymous,
        "selected_categories": [
            CMS.objects.first().category1,
            CMS.objects.first().category2,
            CMS.objects.first().category3,
            CMS.objects.first().category4,
            CMS.objects.first().category5,
            CMS.objects.first().category6,
        ],
        "all_categories": Category.objects.all(),
        "cms": {
            "logo": CMS.objects.first().logo,
            "title": CMS.objects.first().footer_title,
            "description": CMS.objects.first().footer_description,
            "facebook": CMS.objects.first().facebook_url,
            "instagram": CMS.objects.first().instagram_url,
            "twitter": CMS.objects.first().twitter_url,
        },
    }


def _add_read_later_to_news(news, user):
    for article in news:
        try:
            readlater = ReadLater.objects.get(user=user, news=article)
            article.readLater = not readlater.is_removed
        except ReadLater.DoesNotExist:
            article.readLater = False
    return news


def home(request):
    common_vars = _common_vars(request.user.is_anonymous)
    # top news (for main slider)
    top_news = News.objects.all().order_by("-publish_date")[:10]
    # top news in each selected category
    top_categories_news = {
        category: News.objects.filter(is_top_in_category=True, news_category=category)
        for category in common_vars["selected_categories"]
    }
    popular_news = News.objects.all().order_by("-publish_date")[:10]
    if not request.user.is_anonymous:
        popular_news = _add_read_later_to_news(popular_news, request.user)
    return render(
        request,
        "index.html",
        {
            **common_vars,
            "top_news": top_news,
            "top_categories_news": top_categories_news,
            "popular_news": popular_news,
        },
    )


def category(request, category: str):
    category_news = News.objects.filter(
        news_category=Category.objects.get(name=category)
    )[:20]
    if not request.user.is_anonymous:
        category_news = _add_read_later_to_news(category_news, request.user)
    return render(
        request,
        "category_news.html",
        {
            **_common_vars(request.user.is_anonymous),
            "category": category,
            "category_news": category_news,
        },
    )


def article(request, article_id: int):
    return render(
        request,
        "article_details.html",
        {
            **_common_vars(request.user.is_anonymous),
            "article": News.objects.get(id=article_id),
        },
    )


@authenticated_required
def read_later(request):
    read_later = ReadLater.objects.filter(
        user=request.user, is_removed=False
    ).values_list("news_id", flat=True)
    read_later_news = News.objects.filter(id__in=read_later)
    for article in read_later_news:
        article.readLater = True
    return render(
        request,
        "read_later.html",
        {
            **_common_vars(request.user.is_anonymous),
            "read_later_news": read_later_news,
        },
    )


@authenticated_required
def history(request):
    history = History.objects.filter(user=request.user, is_removed=False).values_list(
        "news_id", flat=True
    )
    history_news = News.objects.filter(id__in=history)
    history_news = _add_read_later_to_news(history_news, request.user)
    return render(
        request,
        "history.html",
        {
            **_common_vars(request.user.is_anonymous),
            "history_news": history_news,
        },
    )
